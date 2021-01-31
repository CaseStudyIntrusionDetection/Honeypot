import re
import os
from urllib.parse import unquote
import mimetypes
import multidict
import json
import logging
import aiohttp
from bs4 import BeautifulSoup
from snare.html_handler import HtmlHandler

class TannerHandler():
    def __init__(self, run_args, meta, snare_uuid):
        self.run_args = run_args
        self.meta = meta
        if 'full_page_path' in run_args:
            self.dir = run_args.full_page_path
        self.snare_uuid = snare_uuid
        self.html_handler = HtmlHandler(run_args.no_dorks, run_args.tanner)
        self.logger = logging.getLogger(__name__)

    def create_data(self, request, response_status):
        data = dict(
            method=None,
            path=None,
            headers=None,
            uuid=self.snare_uuid.decode('utf-8'),
            peer=None,
            status=response_status
        )
        if request.transport:
            peer = dict(
                ip=request.transport.get_extra_info('peername')[0],
                port=request.transport.get_extra_info('peername')[1]
            )
            data['peer'] = peer
        if request.path:
            # FIXME request.headers is a CIMultiDict, so items with the same
            # key will be overwritten when converting to dictionary
            header = {key: value for (key, value) in request.headers.items()}
            data['method'] = request.method
            data['headers'] = header
            data['path'] = request.path_qs
            if 'Cookie' in header:
                data['cookies'] = {cookie.split('=')[0].strip(): cookie.split('=')[1]
                                   for cookie in header['Cookie'].split(';')}
        return data

    async def submit_data(self, data):
        event_result = None
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.post(
                    'http://{0}:8090/event'.format(self.run_args.tanner),
                    json=data, timeout=10.0
                )
                try:
                    event_result = await r.json()
                except (json.decoder.JSONDecodeError, aiohttp.client_exceptions.ContentTypeError) as e:
                    self.logger.error('Error submitting data: {} {}'.format(e, data))
                    event_result = {'version': '0.6.0', 'response': {'message': {'detection':
                                    {'name': 'index', 'order': 1, 'type': 1, 'version': '0.6.0'},
                                    'sess_uuid': data['uuid']}}}
                finally:
                    await r.release()
        except Exception as e:
            self.logger.exception('Exception: %s', e)
            raise e
        return event_result
