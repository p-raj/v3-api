from mistralclient.api.httpclient import HTTPClient

from django.conf import settings

# NOTE:
# this seems a little messy, should
# our server be aware of the API gateway in front of it ?
# Nah, don't think so, but let's get it done for now :(
V3__API_GATEWAY = getattr(settings, 'V3__API_GATEWAY')
V3__HOST_MISTRAL = getattr(settings, 'V3__HOST_MISTRAL')

MISTRAL__BASE_URL = '{0}/v2'.format(V3__API_GATEWAY)


class MistralHTTPClient(HTTPClient):
    def __init__(self, base_url=MISTRAL__BASE_URL, **kwargs):
        super(MistralHTTPClient, self).__init__(base_url, **kwargs)

    @staticmethod
    def get_headers(headers):
        headers = headers or {}
        headers.update(**{
            'Host': V3__HOST_MISTRAL
        })
        return headers

    def get(self, url, headers=None):
        return super(MistralHTTPClient, self) \
            .get(url, headers=self.get_headers(headers))

    def post(self, url, body, headers=None):
        return super(MistralHTTPClient, self) \
            .post(url, body, headers=self.get_headers(headers))

    def put(self, url, body, headers=None):
        return super(MistralHTTPClient, self).put(url, body, self.get_headers(headers))

    def delete(self, url, headers=None):
        return super(MistralHTTPClient, self).delete(url, self.get_headers(headers))
