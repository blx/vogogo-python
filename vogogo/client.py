from simplejson import json
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

    See official documentation at: https://docs.vogogo.com/api
    """

    url = 'https://api.vogogo.com/v2'  # Base API URL

    endpoints = {
        'customers': '/customers',
        'customer': '/customer',
        'accounts': '/accounts',
        'accounts_by_currency': '/accounts?currency=%s',
        'verify': '/accounts/%s/verify',
        'auth': '/accounts/auth',
        'transactions': '/transactions',
        'pay': '/pay',
        'charge': '/charge'
    }

    def __init__(self, client_id, client_secret, bearer_token=None):
        """
        `client_id`     str     Your Vogogo client ID
        `client_secret` str     Your Vogogo client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret

        if bearer_token:
            self.set_bearer_token(bearer_token)

    def set_bearer_token(self, bearer_token):
        self.bearer_token = bearer_token

    def get_bearer_token(self):
        return self.bearer_token

    @require_bearer_token
    @property
    def bearer_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.bearer_token)
        }

        return headers

    @property
    def token_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token token=' + str(self.client_secret)
        }

        return headers

    # Endpoints
    def sign_up_customer(self, customer):
        """
        Sign up a customer

        `customer`  dict    Customer attributes as required by vogogo
        """
        
        url = urljoin(self.url, self.endpoints['customers'])
        r = requests.post(url, data=json.dumps(customer), headers=self.token_headers)
        return r.json()

    @require_bearer_token
    def get_customer(self):
        """
        Retrieve customer information. Provide the customer token in the Authorization header
        """

        url = urljoin(self.url, self.endpoints['customer'])
        r = requests.get(url, headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def add_bank_account(self, name, routing, number, currency, auth_token=None):
        """
        Adds a bank account to an existing customer. The customer does not need to be verified yet.
        A customer can have up to five accounts.
        """

        url = urljoin(self.url, self.endpoints['accounts'])
        payload = {
            'name': name,
            'routing': routing,
            'number': number,
            'currency': currency
        }

        if auth_token:
            payload['auth_token'] = auth_token

        r = requests.post(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def verify_micro_deposit(self, account_id, amount):
        """
        Verify the customer controls a bank account by providing the micro deposit amount
        """
        url = urljoin(self.url, self.endpoints['verify']) % account_id
        payload = {
            'amount': amount
        }

        r = requests.post(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def auth_bank_account(self, email, username, password, type):
        """
        Retrieve the customer's bank accounts by querying their online banking service with their online banking credentials.
        The results can be used to add a bank account with the Add Bank Account endpoint.
        Accounts added this way bypass the need to perform and wait for a micro-deposit.
        The customer's banking credentials are never stored.
        The customer does not need to be verified yet.
        """

        url = urljoin(self.url, self.endpoints['auth'])
        payload = {
            'email': email,
            'username': username,
            'password': password,
            'type': type
        }

        r = requests.post(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def get_accounts(self, currency):
        """
        This endpoint can be used to get a list of a customer's wallet and bank accounts. A currency must be specified.
        """

        url = urljoin(self.url, self.endpoints['accounts_by_currency']) % currency
        r = requests.get(url, headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def get_transactions(self, wallet_id):
        """
        This endpoint can be used to get a list of a customer's transactions that are attached to a particular wallet.
        A wallet_id must be specified.
        """

        url = urljoin(self.url, self.endpoints['transactions'])
        payload = {
            'wallet_id': wallet_id
        }
        r = requests.get(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def pay(self, id, account_id, amount, currency, client_ipv4):
        """
        Pay a customer.
        This initiates a financial transaction to move funds from your merchant wallet to a customer's account
        (wallet or bank account).
        """

        url = urljoin(self.url, self.endpoints['pay'])
        payload = {
            'id': id,
            'account_id': account_id,
            'amount': amount,
            'currency': currency,
            'client_ipv4': client_ipv4
        }

        r = requests.post(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()

    @require_bearer_token
    def charge(self, id, account_id, amount, currency, client_ipv4):
        """
        Charge a customer.
        This initiates a financial transaction to move funds from a customer's account
        (wallet or bank account) to your merchant wallet.
        """

        url = urljoin(self.url, self.endpoints['charge'])
        payload = {
            'id': id,
            'account_id': account_id,
            'amount': amount,
            'currency': currency,
            'client_ipv4': client_ipv4
        }

        r = requests.post(url, data=json.dumps(payload), headers=self.bearer_headers)
        return r.json()