import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from config.settings import BINANCE_API_KEY, BINANCE_SECRET_KEY

class BinanceTradingEngine:
    def __init__(self, api_key=BINANCE_API_KEY, secret_key=BINANCE_SECRET_KEY):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.binance.com"
        self.futures_url = "https://fapi.binance.com"

    def _generate_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _send_request(self, method, endpoint, params=None, is_futures=False):
        url = (self.futures_url if is_futures else self.base_url) + endpoint
        if params is None:
            params = {}
        
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif method == 'POST':
            response = requests.post(url, data=params, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, data=params, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return response.json()

    # Spot Trading
    def place_spot_order(self, symbol, side, type, quantity, price=None, stopPrice=None):
        params = {
            'symbol': symbol,
            'side': side,
            'type': type,
            'quantity': quantity,
        }
        if price: params['price'] = price
        if stopPrice: params['stopPrice'] = stopPrice
        if type in ['LIMIT', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT']:
            params['timeInForce'] = 'GTC'
            
        return self._send_request('POST', '/api/v3/order', params)

    # Futures Trading
    def place_futures_order(self, symbol, side, type, quantity, price=None, stopPrice=None, leverage=5):
        # Set leverage first
        self._send_request('POST', '/fapi/v1/leverage', {'symbol': symbol, 'leverage': leverage}, is_futures=True)
        
        params = {
            'symbol': symbol,
            'side': side,
            'type': type,
            'quantity': quantity,
        }
        if price: params['price'] = price
        if stopPrice: params['stopPrice'] = stopPrice
        if type in ['LIMIT', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT']:
            params['timeInForce'] = 'GTC'
            
        return self._send_request('POST', '/fapi/v1/order', params, is_futures=True)

    # Margin Trading
    def place_margin_order(self, symbol, side, type, quantity, price=None, is_isolated='FALSE'):
        params = {
            'symbol': symbol,
            'side': side,
            'type': type,
            'quantity': quantity,
            'isIsolated': is_isolated
        }
        if price: params['price'] = price
        return self._send_request('POST', '/sapi/v1/margin/order', params)

    def get_portfolio_status(self):
        # Simplified portfolio status
        spot_account = self._send_request('GET', '/api/v3/account')
        return spot_account
