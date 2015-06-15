import simplejson as json
from urlparse import urljoin
import requests


def require_bearer_token(func):
    def inner_func(self, *args, **kwargs):
        if not self.bearer_token:
            raise Exception('`%s` method requires `bearer_token`' %
                            func.__name__)
        return func(self, *args, **kwargs)
    return inner_func


class Client(object):
    """
    Vogogo API client https://vogogo.com/

    See official documentation at: http://docs.vogogo.com/payment_api/v2 
    """

    endpoints = {
        'customers': 'customers',
        'customer': 'customer',
        'accounts': 'accounts',
        'accounts_by_currency': 'accounts?currency={:s}',
        'verify': 'accounts/{:s}/verify',
        'auth': 'accounts/auth',
        'transactions': 'transactions',
        'pay': 'pay',
        'charge': 'charge'
    }

    def __init__(self, client_id, client_secret, url):
        """
        `client_id`     str     Your Vogogo client ID (NOTE: Unused)
        `client_secret` str     Your Vogogo client secret
        `url`           str     Vogogo api base endpoint
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.bearer_token = None

    #def set_bearer_token(self, bearer_token):
    #    self.bearer_token = bearer_token
    #
    #def get_bearer_token(self):
    #    return self.bearer_token

    @require_bearer_token
    def bearer_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.bearer_token)
        }

    def token_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Token token=' + str(self.client_secret)
        }

    

    def _request(self, reqfn, endpoint, params, headers=None, endpoint_params=None):
        headers = headers or self.bearer_headers()

        url = urljoin(self.url, self.endpoints[endpoint])
        if endpoint_params:
            url = url.format(*endpoint_params)

        r = reqfn(url,
                  data=json.dumps(params),
                  headers=headers)
        return r.json()

    def _get_request(self, endpoint, params=None, headers=None, endpoint_params=None):
        return _request(requests.get, endpoint, params, headers)

    def _post_request(self, endpoint, params, headers=None, endpoint_params=None):
        return _request(requests.post, endpoint, params, headers)


    # Endpoints
    def sign_up_customer(self, customer):
        """
        Sign up a customer

        `customer`  dict    Customer attributes as required by vogogo
        """
        
        return _post_request('customers', customer, headers=self.token_headers())

    @require_bearer_token
    def get_customer(self):
        """
        Retrieve customer information. Provide the customer token in the Authorization header
        """

        return _get_request('customer')

    @require_bearer_token
    def add_bank_account(self, name, routing, number, currency, auth_token=None):
        """
        Adds a bank account to an existing customer. The customer does not need to be verified yet.
        A customer can have up to five accounts.
        """

        payload = {
            'name': name,
            'routing': routing,
            'number': number,
            'currency': currency
        }

        if auth_token:
            payload['auth_token'] = auth_token

        return _post_request('accounts', payload)

    @require_bearer_token
    def verify_micro_deposit(self, account_id, amount):
        """
        Verify the customer controls a bank account by providing the micro deposit amount
        """

        payload = {
            'amount': amount
        }

        return _post_request('verify', payload, endpoint_params=[account_id])

    @require_bearer_token
    def auth_bank_account(self, email, username, password, type):
        """
        Retrieve the customer's bank accounts by querying their online banking service with their online banking credentials.
        The results can be used to add a bank account with the Add Bank Account endpoint.
        Accounts added this way bypass the need to perform and wait for a micro-deposit.
        The customer's banking credentials are never stored.
        The customer does not need to be verified yet.
        """

        payload = {
            'email': email,
            'username': username,
            'password': password,
            'type': type
        }

        return _post_request('auth', payload)

    @require_bearer_token
    def get_accounts(self, currency):
        """
        This endpoint can be used to get a list of a customer's wallet and bank accounts. A currency must be specified.
        """

        return _get_request('accounts_by_currency', endpoint_params=[currency])

    @require_bearer_token
    def get_transactions(self, wallet_id):
        """
        This endpoint can be used to get a list of a customer's transactions that are attached to a particular wallet.
        A wallet_id must be specified.
        """

        payload = {
            'wallet_id': wallet_id
        }

        return _get_request('transactions', payload)

    @require_bearer_token
    def pay(self, id, account_id, amount, currency, client_ipv4):
        """
        Pay a customer.
        This initiates a financial transaction to move funds from your merchant wallet to a customer's account
        (wallet or bank account).
        """

        payload = {
            'id': id,
            'account_id': account_id,
            'amount': amount,
            'currency': currency,
            'client_ipv4': client_ipv4
        }

        return _post_request('pay', payload)

    @require_bearer_token
    def charge(self, id, account_id, amount, currency, client_ipv4):
        """
        Charge a customer.
        This initiates a financial transaction to move funds from a customer's account
        (wallet or bank account) to your merchant wallet.
        """

        payload = {
            'id': id,
            'account_id': account_id,
            'amount': amount,
            'currency': currency,
            'client_ipv4': client_ipv4
        }

        return _post_request('charge', payload)
