from re import I
from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
from mpesa.api.auth import MpesaBase
app = Flask(__name__)

CONSUMER_SECRET='vNxa1aOwzAfM3Mog'
CONSUMER_KEY='0kWsYE5PZyGcM5QxwpGYxIEAnpIIEl0Y'
SHORT_CODE='600997'
base_url = "http://192.168.1.113:3400/"


@app.route('/apps')
def apps():
    authentication = MpesaBase(
        app_key=CONSUMER_KEY, 
        app_secret=CONSUMER_SECRET, 
        sandbox_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')
    key = authentication.authenticate()
    print(key)
    return key




def gen_access_token():   
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    print('generating access token')
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    print('keys: ', consumer_key, consumer_secret)
    data = (requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))).json()
    print("token generated")
    return data['access_token']


@app.route('/access_token')
def token():
    data = gen_access_token()
    return data


@app.route('/register_urls')
def register_urls():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    access_token = gen_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    request_body = {
        "ShortCode": SHORT_CODE,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{base_url}/c2b/confirm",
        "ValidationURL": f"{base_url}/c2b/validation"
    }
    response_data = requests.post(mpesa_endpoint, json = request_body, headers = headers)
    return response_data.json()

@app.route('/c2b/confirm')
def confirm():
    """
    """
    # get data
    data = request.get_json()
    print(data)
    return {
        "ResultCode": 0,
        "ThirdPartyTransID": "",
        "OrgAccountBalance": "",
        "ResultDesc": "Accepted",
        "FirstName": "",
        "LastName": ""
    }

@app.route('/c2b/validation')
def validation():
    """
    """
    # get data
    data = request.get_json()
    print(data)
    return {
        "ResultCode": 0,
        "ThirdPartyTransID": "",
        "OrgAccountBalance": "",
        "ResultDesc": "Accepted",
        "FirstName": "",
        "LastName": ""
    }


@app.route('/simulate')
def simulate():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    access_token = gen_access_token()
    headers = { "Authorization": f"Bearer {access_token}" }
    request_body = {
        "ShortCode": "",
        "CommandID": "",
        "BillRefNumber": "",
        "Msisdn": "254704231620",
        "Amount": 100
    }
    simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)
    return simulate_response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3400", debug=True)
