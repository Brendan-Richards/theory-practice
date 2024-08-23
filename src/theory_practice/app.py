import os

from flask import Flask, jsonify, request, render_template
from theory_practice.theory_teacher import TheoryTeacher

app = Flask(__name__)

teacher = TheoryTeacher()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-configs/<string:theory_mode>", methods=["GET"])
def get_configs(theory_mode: str):
    theory_mode_cleaned = theory_mode.strip().replace(" ", "_").lower()
    cfg_files = os.listdir(os.path.join("configs", theory_mode_cleaned))
    cfg_files = [x.replace(".toml", "") for x in cfg_files]
    return jsonify(cfg_files)


@app.route("/set-theory-mode/<string:theory_mode>", methods=["GET"])
def set_theory_mode(theory_mode: str):
    theory_mode_cleaned = theory_mode.strip().replace(" ", "_").lower()
    teacher.set_theory_mode(theory_mode_cleaned)
    return "Success"


@app.route("/load-config/<string:config_name>", methods=["GET"])
def load_config(config_name: str):
    teacher.load_config(config_name)
    return "Success"


@app.route("/get-question", methods=["GET"])
def get_question():
    question_data = teacher.generate_question()
    return jsonify(question_data)


@app.route("/submit-answer", methods=["POST"])
def submit_answer():
    results = teacher.grade(request.json)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
