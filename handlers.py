from google.appengine.api import urlfetch
import logging
import traceback
import utils
import json
import constants


class CreateUpdateQuestionBank:
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


class FetchQuestionSet:
    @classmethod
    def get_categories(cls):
        try:
            categories = utils.MemcacheHandler.get_from_memcache(constants.categories_mamcache)
            return json.dumps(categories)

        except Exception as e:
            logging.error(traceback.format_exc())

    @classmethod
    def get_questions(cls, category):
        try:
            question_set = utils.MemcacheHandler.get_from_memcache(constants.category_question_bank_with_solution_memcache_key.format(category))
            if not question_set:
                question_set = utils.MemcacheHandler.set_category_question_set(category)

            return json.dumps(question_set)

        except:
            logging.error(traceback.format_exc())
            return constants.error_message
