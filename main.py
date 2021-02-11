from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def check():
    return {
        'response': '200 Success'
    }


if __name__ == '__main__':
    app.run(debug=True)