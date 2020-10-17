from google.appengine.ext import db
import constants


class QuestionSetModel(db.Model):
    question_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
    correct_answer_id = db.StringProperty()
    question_text = db.TextProperty(default='')
    category = db.StringProperty(default=constants.default_question_category, indexed=True)
    answers = db.ListProperty(item_type=str)


class AnswersModel(db.Model):
    answer_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
    answer_text = db.TextProperty(default='')
    chosen_percentage = db.StringProperty()


class Users(db.Model):
    user_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
    score_sheets = db.ListProperty(item_type=str)


class ScoreSheets(db.Model):
    score_sheet_id = db.StringProperty(default='')
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
    score_sheet = db.TextProperty(default="{}")


