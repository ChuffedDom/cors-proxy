import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return {
        'message': 'Hello World'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)