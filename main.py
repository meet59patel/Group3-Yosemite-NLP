from flask import Flask, request
from flask_cors import CORS
from subjective_answer_checker import predict_Marks

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def check():
    return {
        'response': '200 Success'
    }

@app.route('/predict', methods=['POST'])
def predict():
    request_data = request.get_json()
    model_ans = request_data['model_ans']
    student_ans = request_data['student_ans']
    max_marks = request_data['max_marks']
    result = predict_Marks(model_ans, student_ans, max_marks)
    return {
        'response': result
    }


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)