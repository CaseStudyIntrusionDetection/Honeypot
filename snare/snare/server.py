import logging
import json
import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
from snare.middlewares import SnareMiddleware
from snare.tanner_handler_directory import TannerHandlerDirectory
from snare.tanner_handler_server import TannerHandlerServer
from snare.utils.data_collector import DataCollector

class HttpRequestHandler():
    def __init__(
            self,
            meta,
            run_args,
            snare_uuid,
            is_directory,
            debug=False,
            keep_alive=75,
            **kwargs):
        self.run_args = run_args
        self.is_directory = is_directory
        self.meta = meta
        self.snare_uuid = snare_uuid
        self.logger = logging.getLogger(__name__)
        if is_directory:
            self.tanner_handler = TannerHandlerDirectory(run_args, meta, snare_uuid)
        else:
            self.tanner_handler = TannerHandlerServer(run_args, meta, snare_uuid)
        self.data_collector = DataCollector(run_args.data_collect_path)

    async def submit_slurp(self, data):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                r = await session.post(
                    'https://{0}:8080/api?auth={1}&chan=snare_test&msg={2}'.format(
                        self.run_args.slurp_host, self.run_args.slurp_auth, data
                    ), json=data, timeout=10.0
                )
                assert r.status == 200
                r.close()
        except Exception as e:
            self.logger.error('Error submitting slurp: %s', e)

    async def handle_request(self, request):
        self.logger.info('Request path: {0}'.format(request.path_qs))
        data = self.tanner_handler.create_data(request, 200)
        if request.method == 'POST':
            post_data = await request.post()
            self.logger.info('POST data:')
            for key, val in post_data.items():
                self.logger.info('\t- {0}: {1}'.format(key, val))
            data['post_data'] = dict(post_data)
        else:
            post_data = ""

        # Submit the event to the TANNER service
        event_result = await self.tanner_handler.submit_data(data)

        # Log the event to slurp service if enabled
        if self.run_args.slurp_enabled:
            await self.submit_slurp(request.path_qs)

        content, headers, status_code, emulator = await self.tanner_handler.parse_tanner_response(
            request.path_qs, event_result['response']['message']['detection'], data)

        if self.run_args.server_header:
            headers['Server'] = self.run_args.server_header

        if 'cookies' in data and 'sess_uuid' in data['cookies']:
            previous_sess_uuid = data['cookies']['sess_uuid']
        else:
            previous_sess_uuid = None

        if event_result is not None and\
                'sess_uuid' in event_result['response']['message']:
            cur_sess_id = event_result['response']['message']['sess_uuid']
            if previous_sess_uuid is None or not previous_sess_uuid.strip() or previous_sess_uuid != cur_sess_id:
                headers.add('Set-Cookie', 'sess_uuid=' + cur_sess_id)

        remote_ip, _ = request.transport.get_extra_info('peername')

        self.data_collector.log(request.method, request.rel_url, request.version, request.headers, content,
                emulator, post_data, headers, cur_sess_id, previous_sess_uuid, remote_ip, status_code)

        return web.Response(body=content, status=status_code, headers=headers)

    async def start(self):
        app = web.Application()
        app.add_routes([web.route('*', '/{tail:.*}', self.handle_request)])

        if self.is_directory:
            aiohttp_jinja2.setup(
                app, loader=jinja2.FileSystemLoader(self.run_args.full_page_path)
            )
            middleware = SnareMiddleware(
                error_404=self.meta['/status_404'].get('hash'),
                headers=self.meta['/status_404'].get('headers', []),
                server_header=self.run_args.server_header
            )
            middleware.setup_middlewares(app)

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(
            self.runner,
            self.run_args.host_ip,
            self.run_args.port)

        await site.start()
        names = sorted(str(s.name) for s in self.runner.sites)
        print("======== Running on {} ========\n"
              "(Press CTRL+C to quit)".format(', '.join(names)))

    async def stop(self):
        await self.runner.cleanup()
