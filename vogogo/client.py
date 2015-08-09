# Usage
# 
# vogogo = Client('asdsdg34wesdga', 'https://api.vogogo.com/v3/')
# vogogo.customer('msdgn9123mas').charge_bank_account(...)
# ...


# Python3 / Python2
try:
    from functools import partialmethod
except ImportError:
    from .partialmethod import partialmethod

# Python3 / Python2
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# 3rd party library
try:
    import simplejson as json
except ImportError:
    import json

import requests
from requests.auth import HTTPBasicAuth


API_V3 = 'https://api.vogogo.com/v3/'
API_V3_STAGING = 'https://staging.api.vogogo.com/v3/'

class Client(object):
    """
    Vogogo API client https://vogogo.com/

    See official documentation at: http://docs.vogogo.com/payment_api/v3
    """

    def __init__(self, client_secret, url):
        """
        `client_secret` str     Your Vogogo client secret
        `url`           str     Vogogo api base endpoint
        """
        self.client_secret = client_secret
        self.url = url

        self.auth = HTTPBasicAuth(client_secret, '')
        self.headers = {
            'Content-Type': 'application/json'
        }
    

    def _request(self, verb, path, data=None, headers=None, params=None):
        if not self.auth:
            raise Exception('Authentication required before making any requests.')

        headers = headers or self.headers
        params = params or {}

        url = urljoin(self.url, path)

        reqfn = getattr(requests, verb.lower())
        return reqfn(url,
                     params=params,
                     data=json.dumps(data),
                     headers=headers,
                     auth=self.auth).json()


    # Convenience method for chaining
    def customer(self, customer_id):
        return Customer(self, customer_id)


    # Endpoints
    def sign_up_customer(self, customer):
        """
        Sign up a customer

        `customer`  dict    Customer attributes as required by vogogo
        """
        
        return self._request('post', 'customers', data=customer)


    def list_customers(self, params=None):
        return self._request('get', 'customers', params=params)


    def list_industry_types(self):
        return self._request('get', 'industry_types')

    def list_occupations(self):
        return self._request('get', 'occupations')



class Customer(object):
    def __init__(self, client, customer_id):
        self.client = client
        self.id = customer_id

    def _request(self, verb, path, *args, **kwargs):
        path = ['customers', self.id] + (path or [])
        path = '/'.join(map(str, path))
        return self.client._request(verb, path, *args, **kwargs)

    _get = partialmethod(_request, 'get')
    _post = partialmethod(_request, 'post')
    _patch = partialmethod(_request, 'patch')
    _delete = partialmethod(_request, 'delete')


    def get(self):
        return self._get(path='')

    def update(self, data):
        return self._patch(path='',
                           data=data)


    def create_bank_account(self, data):
        return self._post(['bank_accounts'],
                          data=data)

    def verify_micro_deposit(self, account_id, data):
        return self._post(['bank_accounts', account_id, 'micro_verifications'],
                          data=data)

    def delete_bank_acount(self, account_id):
        return self._delete(['bank_accounts', account_id])


    def get_account(self, account_id):
        return self._get(['accounts', account_id])

    def list_accounts(self):
        return self._get(['accounts'])


    def charge_bank_account(self, data):
        return self._post(['bank'],
                          data=data)

    def pay_bank_account(self, data):
        return self._post(['bank'],
                          data=data)

    def get_bank_transaction(self, transaction_id):
        return self._get(['bank',
                         transaction_id])

    def list_bank_transactions(self, params=None):
        return self._get(['bank'],
                         params=params)


    def charge_card(self, data):
        return self._post(['card'],
                          data=data)

    def get_card_transaction(self, transaction_id):
        return self._get(['card', transaction_id])

    def list_card_transactions(self, params=None):
        return self._get(['card'],
                         params=params)


    def charge_interac(self, data):
        return self._post(['interac'],
                          data=data)

    def get_interac_transaction(self, transaction_id):
        return self._get(['interac', transaction_id])

    def list_interac_transactions(self, params=None):
        return self._get(['interac'],
                         params=params)

    
    def get_transaction(self, transaction_id):
        return self._get(['transactions', transaction_id])

    def list_transactions(self, params=None):
        return self._get(['transactions'],
                         params=params)
