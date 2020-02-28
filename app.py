import flask
from flask import Flask, jsonify
from flask import request
from model.train_classifier import find_skill
from main import base_skill_finder

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello"


@app.route('/currentUser', methods=['GET'])
def current_user():
    response = flask.jsonify({'username': 'Kait'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route("/askQuestion", methods=['GET'])
def ask_question():
    user_input = request.args.get('userInput', type=str)
    found_skill = find_skill(user_input)
    output = base_skill_finder(found_skill, user_input)
    response = flask.jsonify({'message': output})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)