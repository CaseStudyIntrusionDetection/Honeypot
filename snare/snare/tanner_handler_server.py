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
from snare.tanner_handler import TannerHandler

class TannerHandlerServer(TannerHandler):

    async def make_request(self, data):
        # create returns (if request fails)
        content, headers, status_code = "", multidict.CIMultiDict(), 500
        # no cookies => empty dict
        if not 'cookies' in data:
            data['cookies'] = {}
        # clean up headers
        send_headers = multidict.CIMultiDict(data['headers'])
        for key in [ 'Host', 'Origin',  'Content-Length', 'Connection', 'Cookie' 'Accept-Encoding', 'Content-MD5', 'TE', 'Transfer-Encoding', 'Upgrade' ]:
            if key in send_headers:
                del send_headers[key]
        # create connection
        async with aiohttp.ClientSession(cookies=data['cookies'], headers=send_headers, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            # calculate url
            proxy_url = self.run_args.page_location + ( data['path'] if data['path'][0] != '/' else data['path'][1:] )

            # do GET or POST
            if data['method'] == 'GET':
                r = await session.get(proxy_url, timeout=10.0)
            else:
                r = await session.post(proxy_url, data=data['post_data'], timeout=10.0)

            status_code = r.status
            headers = r.headers
            content = await r.read()

            await r.release()

            headers = multidict.CIMultiDict(headers)
            for key in ['Transfer-Encoding','Connection', 'Trailer', 'Vary']:
                if key in headers:
                    del headers[key]

        return content, headers, status_code

    async def parse_tanner_response(self, requested_name, detection, data):
        # proxying
        content, headers, status_code = await self.make_request(data)
        
        # Creating a regex object for the pattern of multiple contiguous forward slashes
        p = re.compile('/+')
        # Substituting all occurrences of the pattern with single forward slash
        requested_name = p.sub('/', requested_name)

        if detection['type'] == 1:
            emulator = "none" # no emulator used cause no attack detected

        elif detection['type'] == 2:
            payload_content = detection['payload']
            if payload_content['page']:
                soup = BeautifulSoup(content, 'html.parser')
                script_tag = soup.new_tag('div')
                script_tag.append(
                    BeautifulSoup(
                        payload_content['value'],
                        'html.parser'))
                soup.body.append(script_tag)
                content = str(soup).encode()
            else:
                headers['Content-Type'] = 'text/plain'
                content = payload_content['value'].encode('utf-8')

            if 'headers' in payload_content:
                # overwrite local headers with the tanner-provided ones
                headers.update(payload_content['headers'])

            emulator = detection['name'] # get the (short) name of the used emulator 

        else:  # type 3
            status_code = detection['payload']['status_code']

            emulator = "error" # error while using emulator (check tanner!!)


        return content, headers, status_code, emulator
