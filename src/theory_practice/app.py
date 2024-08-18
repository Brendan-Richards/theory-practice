import os

from flask import Flask, jsonify, request, render_template
from theory_practice.theory_teacher import TheoryTeacher

app = Flask(__name__)

teacher = TheoryTeacher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-question', methods=['GET'])
def get_question():
    print("hello")
    return {"hello": "apple"}
    # question_data = teacher.generate_question()  # Implement this method in TheoryTeacher
    # return jsonify(question_data)

@app.route('/get-configs/<string:theory_mode>', methods=['GET'])
def get_configs(theory_mode: str):

    # data = request.json
    print(theory_mode)
    # os.listdir("")
    return {"hello": "apple"}


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    print(data)
    return "hello"
    # correct = teacher.check_answer(data['guess'], data['question_data'])
    # return jsonify({'correct': correct})

if __name__ == '__main__':
    app.run(debug=True)