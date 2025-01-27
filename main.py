import flask

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)