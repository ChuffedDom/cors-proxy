from flask import Flask, request
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, debug=True)

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.before_request
def before_request():
    """Force HTTPS in Flask if behind a proxy."""
    if request.headers.get("X-Forwarded-Proto") == "http":
        return {"error": "Please use HTTPS"}, 403

@app.route('/', methods=['GET'])
def health_check():
    logging.info("Health check endpoint hit")
    return {
        'message': 'API is working'
    }

@app.route('/mirror', methods=['POST'])
def mirror():
    # Log incoming request
    logging.info(f"Mirror endpoint hit with data: {request.json}")
    return {
        'request-sent': request.json
    }

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    logging.info(f"Proxy endpoint hit with data: {request.json}")
    req_data = request.json
    target = req_data.get('target')
    body = req_data.get('body')

    if not target or not body:
        logging.error("Missing 'target' or 'body' field in request")
        return {
            'error': 'Missing required fields in request'}, 400

    # Send the body to the target as a proxy
    try:
        response = requests.post(target, json=body)
        logging.info(f"Response from {target}: {response.status_code} - {response.json()}")
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': 'Failed to proxy the request'
            }, response.status_code
    except Exception as e:
        logging.error(f"Error in proxying: {e}")
        return {
            'error': 'Failed to proxy the request'
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
