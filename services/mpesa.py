import requests, os, base64, string
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def authenticate() -> str:
    """
    It takes the base_64 encoded string and sends it to the safaricom API to get an access token
    :return: The access token is being returned
    """
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
    querystring = {"grant_type": "client_credentials"}
    payload = ""
    base_64 =  os.getenv('BASE_64')
    headers = {
        "Authorization": "Basic " + base_64
    }

    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring)
    data = response.json()  
    access_token = data['access_token']
    return access_token

def time_stamp() -> str:
    """
    It takes the current date and time, converts it to a timestamp, converts the timestamp back to a
    date and time, and then removes all punctuation from the date and time.
    :return: A string of the current date and time in the format YYYY-MM-DDHH:MM:SS
    """
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    dt2 = datetime.fromtimestamp(ts).strftime("%Y-%m-%d%H:%M:%S")
    timestamp = str(dt2)
    
    for punctuation in string.punctuation:
        timestamp = timestamp.replace(punctuation, "")
    return timestamp

def encoder() -> str:
    """
    It takes the BusinessShortCode, passkey and timestamp and encodes them into a base64 string.
    :return: The encoded password is being returned.
    """
    BusinessShortCode = os.getenv('BUSINESS_CODE')
    timestamp = time_stamp()
    passkey = os.getenv('PASSKEY')
    password_bytes = (BusinessShortCode + passkey + timestamp).encode('utf-8')
    base_64_encoded_string = base64.b64encode(password_bytes)
    base_64_encoded_string = base_64_encoded_string.decode('utf-8')
    return base_64_encoded_string
        
def stk_push() -> str:
    """
    The function takes the access token, time stamp, password and the request body and sends a POST
    request to the url
    """
    query_string = {}
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    access_token = authenticate()
    request_body = {
        "BusinessShortCode": os.getenv('BUSINESS_CODE'),
        "Password": encoder(),
        "Timestamp": time_stamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": os.getenv('PHONE_NUMBER'),
        "PartyB": os.getenv('BUSINESS_CODE'),
        "PhoneNumber": os.getenv('PHONE_NUMBER'),
        "CallBackURL": "https://darajambili.herokuapp.com/express-payment",
        "AccountReference": "0112356789",
        "TransactionDesc": "Pay bill"
    }

    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, json=request_body, headers=headers, params=query_string
    ).json()
    return response.get('ResponseDescription')

