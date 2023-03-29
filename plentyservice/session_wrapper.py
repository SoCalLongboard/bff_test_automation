from requests.auth import HTTPBasicAuth
import requests


class SessionWrapper(requests.Session):
    def __init__(self, url_base, api_key, api_secret, *args, **kwargs):
        super(SessionWrapper, self).__init__(*args, **kwargs)
        self.url_base = url_base
        self.auth = HTTPBasicAuth(api_key, api_secret)

    def request(self, method, url, **kwargs):
        modified_url = self.url_base + url
        print(f"Session request {method} {modified_url}")

        return super(SessionWrapper, self).request(method, modified_url, **kwargs)
