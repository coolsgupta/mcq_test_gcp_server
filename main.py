from flask import Flask
from flask import request
from handlers import *
from flask_cors import CORS
import constants
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/create_update_question_bank')
def create_update_question_bank():
    return CreateUpdateQuestionBank.get()


@app.route('/fetch_question_set')
def fetch_complete_question_set():
    return FetchQuestionSet.get_questions(request.args.get(constants.question_category, 'ALL'))


if __name__ == '__main__':
    app.run()
