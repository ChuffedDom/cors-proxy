import logging
import flask
import requests
from flask_cors import CORS

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return {
        'message': 'API is working'
    }

@app.route('/mirror', methods=['POST'])
def mirror():
    # repeat the incoming request body as the response body with the key "request-sent"
    return {
        'request-sent': flask.request.json
    }

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    
    request = flask.request.json
    target = request.get('target')
    body = request.get('body')
    # send the body to the target as a proxy
    response = requests.post(target, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            'error': 'Failed to proxy the request'
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)