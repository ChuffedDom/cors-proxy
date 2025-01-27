import flask
import requests
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5500"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5500"  # Match the client origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"  # Explicitly allow credentials
    return response

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

@app.route('/proxy', methods=['POST'])
def proxy():
    if flask.request.method == 'OPTIONS':
        return '', 204  # Respond to the preflight request
    
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