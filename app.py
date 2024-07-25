import os
from flask import Flask, request, jsonify
import requests
import jwt

app = Flask(__name__)

@app.route('/')
def home():
    if 'X-MS-CLIENT-PRINCIPAL-NAME' in request.headers:
        return f"Hello, {request.headers['X-MS-CLIENT-PRINCIPAL-NAME']}!"
    else:
        return "Please log in."

@app.route('/api/user')
def get_user_info():
    headers = {k: v for k, v in request.headers if k.startswith('X-MS-CLIENT-PRINCIPAL')}
    return jsonify(headers)

@app.route('/api/claims')
def get_claims():
    token_header = request.headers.get('X-MS-TOKEN-AAD-ID-TOKEN')
    if not token_header:
        return jsonify({"error": "No token found"}), 401
    
    try:
        # In a production app, you should validate the token here
        claims = jwt.decode(token_header, options={"verify_signature": False})
        return jsonify(claims)
    except jwt.DecodeError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)