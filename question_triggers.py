import json


class QuestionTriggers(object):
    questions = {
        'location_trigger': '¿Dónde vives?'
    }

    def __init__(self, json_content=None):
        if json_content and type(json_content) == str:
            self.questions = json.loads(json_content)
        elif json_content and type(json_content) == dict:
            self.questions = json_content
