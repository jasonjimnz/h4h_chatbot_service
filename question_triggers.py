import json


class QuestionTriggers(object):
    questions = {
        'location_trigger': '¿Dónde vives?',
        'ela_question_1': """¿Como definirías tu proceso de habla?\n
        1	Proceso de habla normal\n
        2	Desorden detectable del habla\n	
        3	Inteligible con repetición\n
        4	Habla combinada con comunicación no vocal\n	
        5	Pérdida de habla útil\n
        """,
        'ela_question_2': """¿Como definirías tu proceso de salivación?\n
        1	Normal\n
        2	Ligero exceso de saliva en boca, puede haber babeo nocturno\n	
        3	Exceso de saliva moderado, puede haber babeo matinal\n
        4	Marcado exceso de saliva con algo de babeo\n	
        5	Marcado babeo, requiere constante limpieza con pañuelo\n
            """
    }

    def __init__(self, json_content=None):
        if json_content and type(json_content) == str:
            self.questions = json.loads(json_content)
        elif json_content and type(json_content) == dict:
            self.questions = json_content
