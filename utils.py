import data_models
import logging
import traceback
from google.appengine.api import memcache
import json
import constants

class MemcacheHandler:
    @classmethod
    def get(cls, memcache_key):
        try:
            data = memcache.get(memcache_key)
            return json.loads(data)

        except:
            logging.warning(traceback.format_exc())
            return None

    @classmethod
    def set_category_question_set(cls, memcache_key):
        category = memcache_key.split('_')[0]
        data_object = data_models.QuestionSetModel.all()
        if category != 'ALL':
            data_object = data_object.filter('category', category)

        question_data_obj = data_object.fetch(None)

        try:
            answers_dict = cls.get(constants.answers_memcache_key)
            if not answers_dict:
                answers_dict = cls.set_answers_memcache()

        except:
            logging.error(traceback.format_exc())
            raise Exception('Unable to load answers')

        question_list = []
        for question_obj in question_data_obj:
            question_list.append({
                constants.question_id: question_obj.question_id,
                constants.question_category: question_obj.category,
                constants.correct_answer_id: question_obj.correct_answer_id,
                constants.question_text: question_obj.question_text,
                constants.answers: [answers_dict[answer_id] for answer_id in question_obj.answers]
            })

        memcache.set(memcache_key, json.dumps(question_list))
        return question_list

    @classmethod
    def set_answers_memcache(cls):
        all_answers_dict = {}
        all_answers = data_models.AnswersModel.all().fetch(None)
        for answer in all_answers:
            all_answers_dict[answer.answer_id] = {answer.answer_id:answer.answer_text}

        memcache.set(constants.answers_memcache_key, json.dumps(all_answers_dict))
        return all_answers_dict


def insert_update_question_bank_db(question_set):
    for question in question_set:
        question_id = question['id']
        try:
            question_record = data_models.QuestionSetModel.get_by_key_name(question_id)

        except:
            logging.warning(traceback.format_exc())
            question_record = None

        if not question_record:
            question_record = data_models.QuestionSetModel(key_name=question_id)

        question_record.question_id = question_id
        question_record.question_text = question['question_text']
        question_record.category = question['category']
        question_record.correct_answer_id = question['correct_answer_id']

        for answer in question['answers']:
            answer_id = answer['id']
            try:
                answer_record = data_models.AnswersModel.get_by_key_name(answer_id)

            except:
                logging.warning(traceback.format_exc())
                answer_record = None

            if not answer_record:
                answer_record = data_models.AnswersModel(key_name=answer_id)

            answer_record.answer_id = answer_id
            answer_record.answer_text = answer['answer_text']
            answer_record.chosen_percentage = answer['chosen_percentage']
            answer_record.put()

            if answer_id not in question_record.answers:
                question_record.answers.append(answer_id)

        question_record.put()




