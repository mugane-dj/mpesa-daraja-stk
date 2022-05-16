from types import NoneType
import unittest, sys, os, base64
fpath = os.path.join(os.path.dirname(__file__), '../services')
sys.path.append(fpath)

from mpesa import Mpesa
from datetime import datetime
import string
from dotenv import load_dotenv
load_dotenv()
class TestMpesa(unittest.TestCase):
    def setUp(self):
        self.mpesa = Mpesa()

    def tearDown(self):
        pass

    def test_time_stamp(self):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        dt2 = datetime.fromtimestamp(ts).strftime("%Y-%m-%d%H:%M:%S")
        timestamp = str(dt2)
        for punctuation in string.punctuation:
            timestamp = timestamp.replace(punctuation, "")
        self.assertEqual(timestamp, self.mpesa.time_stamp())

    def test_encoder(self):
        BusinessShortCode = os.getenv('BUSINESS_CODE')
        timestamp = self.mpesa.time_stamp()
        passkey = os.getenv('PASSKEY')
        password_bytes = (BusinessShortCode + passkey + timestamp).encode('utf-8')
        base_64_encoded_string = base64.b64encode(password_bytes)
        base_64_encoded_string = base_64_encoded_string.decode('utf-8')
        self.assertEqual(base_64_encoded_string, self.mpesa.encoder())

    def test_authenticate(self):
        access_token = self.mpesa.authenticate()
        self.assertEqual(type(access_token), str)
        self.assertEqual(len(access_token), 28)
        
    def test_stk_push(self):
        response = self.mpesa.stk_push()
        self.assertEqual('0', response)
        self.assertNotEqual(type(response), NoneType)

if __name__ == '__main__':
    unittest.main()