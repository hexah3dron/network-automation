import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

class PanoramaAPI:
    def __init__(self, host, api_key=None, username=None, password=None, verify_ssl=False):
        self.host = host.rstrip('/')
        self.api_key = api_key
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl

        # if api_key is null, call get_api_key and generate one
        if not self.api_key and self.username and self.password:
            self.api_key = self.get_api_key()

    def get_api_key(self):
        params = {
            'type': 'keygen',
            'user': self.username,
            'password': self.password
        }
        url = f"https://{self.host}/api/?{urlencode(params)}"
        response = requests.get(url, verify=self.verify_ssl)
        parsed_response = ET.fromstring(response.text)

        # parse the XML to determine if the request response was valid
        if parsed_response.attrib['status'] != 'success':
            raise Exception("Failed to retrieve API key")
        # return the key in the parsed_response XML doc
        print(parsed_response.find('./result/key').text)
        return parsed_response.find('./result/key').text

    def make_request(self, params, xpath=None, data=None):
        url = f"https://{self.host}/api/"

        if xpath:
            params['xpath'] = xpath

        if data:
            params['element'] = data

        params['key'] = self.api_key

        response = requests.get(url, params=params, verify=self.verify_ssl)
        parsed_response = ET.fromstring(response.text)

        if parsed_response.attrib['status'] != 'success':
            error_msg = parsed_response.findtext('./msg')
            raise Exception(f"API call failed: {error_msg}")

        return parsed_response

    def get_config(self, xpath):
        params = {'type': 'config', 'action': 'get'}
        return self.make_request(params, xpath)

    def set_config(self, xpath, data):
        params = {'type': 'config', 'action': 'set'}
        return self.make_request(params, xpath, data)

    def commit(self):
        params = {'type': 'commit', 'cmd': '<commit></commit>'}
        return self.make_request(params)

    def push_to_device_group(self, device_group):
        params = {
            'type': 'commit',
            'action': 'all',
            'cmd': f"<commit-all><shared-policy><device-group><entry name='{device_group}'/></device-group></shared-policy></commit-all>"
        }
        return self.make_request(params)