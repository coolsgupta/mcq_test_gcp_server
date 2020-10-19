from google.appengine.api import urlfetch
import logging
import traceback
import utils
import json
import constants
import data_models
import uuid


class UserDatahandler:
    @classmethod
    def register_user(cls, request):
        try:

            logging.info(request.data)
            request_data = json.loads(request.data)
            user_email = request_data[constants.user_email]

            user_data_object = data_models.Users(key_name=user_email)
            if not user_data_object:
                user_data_object = data_models.Users(key_name=user_email)
                user_data_object.put()

            return json.dumps({'success': True})

        except Exception as e:
            logging.error(traceback.format_exc())
            response = {'success': False}
            response['error'] = str(e)
            return json.dumps(response)


class QuestionBankHandler:
    @classmethod
    def get(cls):
        try:
            response = urlfetch.fetch('http://lsatmaxadmin.us/interview/loadData.php', method='GET')
            if response.status_code != 200:
                raise Exception(response.text)

            utils.insert_update_question_bank_db(json.loads(response.content, encoding='utf-8'))

            return "DB Updated"

        except Exception as e:
            logging.error(traceback.format_exc())
            response = {'success': False}
            response['error'] = str(e)
            return json.dumps(response)

    @classmethod
    def get_categories(cls):
        try:
            categories = utils.MemcacheHandler.get_from_memcache(constants.categories_mamcache)
            if not categories:
                cls.get()
                categories = utils.MemcacheHandler.get_from_memcache(constants.categories_mamcache)

            response = {'success': True}
            response['data'] = categories
            return json.dumps(response)

        except Exception as e:
            logging.error(traceback.format_exc())
            response = {'success': False}
            response['error'] = str(e)
            return json.dumps(response)

    @classmethod
    def get_questions(cls, category):
        try:
            question_set = utils.MemcacheHandler.get_from_memcache(constants.category_question_bank_memcache_key.format(category))
            if not question_set:
                question_set = utils.MemcacheHandler.set_category_question_set(category)

            response = {'success': True}
            response['data'] = question_set
            return json.dumps(question_set)

        except:
            logging.error(traceback.format_exc())
            response = {'success': False}
            response['error'] = constants.error_message
            return json.dumps(response)


class ScoreReportHandler:
    @classmethod
    def save_score_sheet(cls, score_sheet):
        score_sheet_id = str(uuid.uuid4())
        score_report_object = data_models.ScoreSheets(key_name=score_sheet_id)
        score_report_object.score_sheet_id = score_sheet_id
        score_sheet['Date'] = score_report_object.modified_at.strftime("%m/%d/%Y, %H:%M")
        score_report_object.score_sheet = json.dumps(score_sheet)
        score_report_object.put()

        return score_sheet_id

    @classmethod
    def add_new_score_sheet(cls, user_email, score_sheet_id):
        user_db_record = data_models.Users.get_by_key_name(user_email)
        user_db_record.score_sheets.append(score_sheet_id)
        user_db_record.put()

    @classmethod
    def get_solutions(cls):
        solutions = utils.MemcacheHandler.get_from_memcache(constants.solution_set)
        if not solutions:
            solutions = utils.MemcacheHandler.set_solution_memcache()

        return solutions

    @classmethod
    def evaluate_response(cls, request):
        try:
            solution_set = cls.get_solutions()
            logging.info(request.data)

            request_data = json.loads(request.data)
            user_response = request_data[constants.user_response]
            user_email = request_data[constants.user_email]
            category_selected = request_data[constants.category_selected]
            logging.info(user_response)

            score = 0
            unattempted = 0
            for key in user_response:
                if user_response[key] is None:
                    unattempted += 1
                    continue

                if solution_set.get(key, '-1') == user_response[key]:
                    score += 1

            score_sheet = {
                'category_selected': category_selected,
                'score': score,
                'unattempted': unattempted,
                'total_questions': len(user_response),
                'wrong': len(user_response) - score - unattempted
            }

            cls.add_new_score_sheet(user_email, cls.save_score_sheet(score_sheet))

            response = {'success': True}
            response['score_sheet'] = score_sheet

            return json.dumps(response)

        except Exception as e:
            response = {'success': False}
            response['error'] = str(e)
            return json.dumps(response)

    @classmethod
    def get_all_score_reports(cls, user_email):
        try:
            if not user_email:
                raise Exception('User Email required')

            user_data_object = data_models.Users.get_by_key_name(user_email)
            user_score_sheets = []
            for score_sheet_id in user_data_object.score_sheets:
                score_sheet_object = data_models.ScoreSheets.get_by_key_name(score_sheet_id)
                user_score_sheets.append(json.loads(score_sheet_object.score_sheet))

            response = {'success': True}
            response['data'] = user_score_sheets

            return json.dumps(response)

        except Exception as e:
            logging.error(traceback.format_exc())
            response = {'success': False}
            response['error'] = str(e)
            return json.dumps(response)

