import unittest, sys, os
fpath = os.path.join(os.path.dirname(__file__), '../services')
sys.path.append(fpath)

from mpesa import Mpesa
from unittest.mock import patch
from datetime import datetime

class TestMpesa(unittest.TestCase):
    def setUp(self):
        self.mpesa = Mpesa()
    def tearDown(self):
        pass
    def test_authenticate(self):
        with patch('mpesa.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'access_token': 'access_token'}
    def test_stk_push(self):
        with patch('mpesa.requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {'ResponseCode': 'ResponseCode', 'ResponseDescription': 'ResponseDescription'}
if __name__ == '__main__':
    unittest.main()