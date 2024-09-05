import requests

class TenantAPI:

    """
    A client holding an authenticated Kobai session to execute CRUD functions on Kobai configuration.
    """

    def __init__(self, token: str, base_uri: str, verify: str | bool = True, proxy: any = None):

        """
        Initialize the TenantAPI client.
        
        Parameters:
        token (str): Kobai application bearer token.
        """
        self.token = token
        self.base_uri = base_uri
        self.session = requests.Session()

        if token is not None:
            self.session.headers.update({'Authorization': 'Bearer %s' % self.token})

        self.session.verify = verify
        if proxy is not None:
            self.session.proxy = proxy

    def __run_post(self, uri, payload, op_desc=None):

        """
        Run a POST call against the authenticated API session.

        Parameters:
        uri (string): Relative service URI to call
        payload (any): Dict to pass to "json" service parameter.
        """

        if op_desc is None:
            op_desc = "operation"

        response = self.session.post(
            self.base_uri + uri,
            #headers={'Authorization': 'Bearer %s' % self.token},
            json=payload,
            timeout=5000
        )
        if response.status_code != 200:
            print(response)
            raise Exception(op_desc +" failed")
        return response

    def __run_get(self, uri, params=None, op_desc=None):

        """
        Run a GET call against the authenticated API session.

        Parameters:
        uri (string): Relative service URI to call
        """

        if op_desc is None:
            op_desc = "operation"

        response = self.session.get(
            self.base_uri + uri,
            params=params,
            #headers={'Authorization': 'Bearer %s' % self.token},
            timeout=5000
        )
        if response.status_code != 200:
            print(response)
            raise Exception(op_desc + " failed")
        return response