from flask import Flask, request
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

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
    logging.info(f"Proxy endpoint hit with data: {request.json}")
    req_data = request.json
    target = req_data.get('target')
    body = req_data.get('body')

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
