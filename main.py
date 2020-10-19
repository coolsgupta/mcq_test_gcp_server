from flask import Flask
from flask import request
from handlers import *
from flask_cors import CORS
import constants
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    # todo: attach reach build
    return 'Hello World!'


@app.route('/register_user', methods=["GET", "POST"])
def register_user():
    return UserDatahandler.register_user(request)


@app.route('/create_update_question_bank')
def create_update_question_bank():
    return QuestionBankHandler.get()


@app.route('/get_categories')
def get_categories():
    return QuestionBankHandler.get_categories()


@app.route('/fetch_question_set')
def fetch_question_set():
    return QuestionBankHandler.get_questions(request.args.get(constants.question_category, 'ALL'))


@app.route('/evaluate_response', methods=["GET", "POST"])
def evaluate_response():
    return ScoreReportHandler.evaluate_response(request)


@app.route('/get_user_score_reports')
def get_user_score_reports():
    return ScoreReportHandler.get_all_score_reports(request.args.get(constants.user_email, None))


if __name__ == '__main__':
    app.run()
