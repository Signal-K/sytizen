from flask import Flask, request, make_response, jsonify
from thirdweb.types import LoginPayload
from thirdweb import ThirdwebSDK
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return "Hello World"

@app.route('/login', methods=['POST'])
def login():
    private_key = os.environ.get("PRIVATE_KEY")
    
    if not private_key:
        print("Missing PRIVATE_KEY environment variable")
        return "Wallet private key not set", 400

    sdk = ThirdwebSDK.from_private_key(private_key, 'mumbai') # Initialise the sdk using the wallet and on mumbai testnet chain
    payload = LoginPayload.from_json(request.json['payload'])

    # Generate access token using signed payload
    domain = 'sailors.skinetics.tech'
    token = sdk.auth.generate_auth_token(domain, payload)

    res = make_response()
    res.set_cookie(
        'access_token',
        token,
        path='/',
        httponly=True,
        secure=True,
        samesite='strict',
    )
    return res, 200

@app.route('/authenticate', methods=['POST'])
def authenticate():
    private_key = os.environ.get("PRIVATE_KEY")
    
    if not private_key:
        print("Missing PRIVATE_KEY environment variable")
        return "Wallet private key not set", 400

    sdk = ThirdwebSDK.from_private_key(private_key, 'mumbai')

    # Get access token from cookies
    token = request.cookies.get('access_token')
    if not token:
        return 'Unauthorised', 401
    
    domain = 'sailors.skinetics.tech'

    try:
        address = sdk.auth.authenticate(domain, token)
    except:
        return "Unauthorized", 401
    
    print(jsonify(address))
    return jsonify(address), 200

@app.route('/logout', methods=['POST'])
def logout():
    res = make_response()
    res.set_cookie(
        'access_token',
        'none',
        expires=datetime.utcnow() + timedelta(second = 5)
    )
    return res, 200