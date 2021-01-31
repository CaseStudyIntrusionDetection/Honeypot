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

class TannerHandlerDirectory(TannerHandler):

    async def parse_tanner_response(self, requested_name, detection, data):
        content = None
        status_code = 200
        headers = multidict.CIMultiDict()
        # Creating a regex object for the pattern of multiple contiguous forward slashes
        p = re.compile('/+')
        # Substituting all occurrences of the pattern with single forward slash
        requested_name = p.sub('/', requested_name)

        if detection['type'] == 1:
            possible_requests = [requested_name]
            query_start = requested_name.find('?')
            if query_start != -1:
                possible_requests.append(requested_name[:query_start])

            file_name = None
            for requested_name in possible_requests:
                if requested_name == '/':
                    requested_name = self.run_args.index_page
                if requested_name[-1] == '/':
                    requested_name = requested_name[:-1]
                requested_name = unquote(requested_name)
                try:
                    file_name = self.meta[requested_name]['hash']
                    for header in self.meta[requested_name].get('headers', []):
                        for key, value in header.items():
                            headers.add(key, value)
                    # overwrite headers with legacy content-type if present and not none
                    content_type = self.meta[requested_name].get('content_type')
                    if content_type:
                        headers['Content-Type'] = content_type
                except KeyError:
                    pass
                else:
                    break

            if not file_name:
                status_code = 404
            else:
                path = os.path.join(self.dir, file_name)
                if os.path.isfile(path):
                    with open(path, 'rb') as fh:
                        content = fh.read()
                    if headers.get('Content-Type', '').startswith('text/html'):
                        content = await self.html_handler.handle_content(content)

            emulator = "none" # no emulator used cause no attack detected

        elif detection['type'] == 2:
            payload_content = detection['payload']
            if payload_content['page']:
                try:
                    file_name = self.meta[payload_content['page']]['hash']
                    for header in self.meta[payload_content['page']].get('headers', []):
                        for key, value in header.items():
                            headers.add(key, value)
                    # overwrite headers with legacy content-type if present and not none
                    content_type = self.meta[payload_content['page']].get('content_type')
                    if content_type:
                        headers['Content-Type'] = content_type
                    page_path = os.path.join(self.dir, file_name)
                    with open(page_path, encoding='utf-8') as p:
                        content = p.read()
                except KeyError:
                    content = '<html><body></body></html>'
                    headers['Content-Type'] = 'text/html'

                soup = BeautifulSoup(content, 'html.parser')
                script_tag = soup.new_tag('div')
                script_tag.append(
                    BeautifulSoup(
                        payload_content['value'],
                        'html.parser'))
                soup.body.append(script_tag)
                content = str(soup).encode()
            else:
                content_type = 'text/plain'
                if content_type:
                    headers['Content-Type'] = content_type
                content = payload_content['value'].encode('utf-8')

            if 'headers' in payload_content:
                # overwrite local headers with the tanner-provided ones
                headers.update(payload_content['headers'])

            emulator = detection['name'] # get the (short) name of the used emulator 

        else:  # type 3
            payload_content = detection['payload']
            status_code = payload_content['status_code']

            emulator = "error" # error while using emulator (check tanner!!)

        return content, headers, status_code, emulator
