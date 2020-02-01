from flask import Flask, request, jsonify
import json
from wit import Wit
from flask_cors import CORS
from config import SERVER, WIT_AI, NEO4J
from graph_data import GraphInstance
from question_triggers import QuestionTriggers
app = Flask(__name__)
CORS(app)

wit_client = Wit(WIT_AI['API_KEY'])
wit_client.message('Hola mundo')

questions = QuestionTriggers()
graph = GraphInstance(**NEO4J)


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'name': 'Hack For Humanity'
    })


@app.route('/trigger/<string:event_name>', methods=['GET'])
def get_event_triger(event_name):
    return jsonify({
        'question': questions.questions.get(event_name, 'Hola')
    })


@app.route('/talk', methods=['POST'])
def talk_action():
    text = request.form.get('text')
    user_id = request.form.get('user_id')
    question_context_tag = request.form.get('question_context_tag')
    callback = None
    if (text):
        response_text = 'En proceso....'
        if question_context_tag == 'ela_question_1':
            ela_questions = {
                "1": "Proceso de habla normal",
                "2": "Desorden detectable del habla",
                "3": "Inteligible con repetición",
                "4": "Habla combinada con comunicación no vocal",
                "5": "Pérdida de habla útil",
            }
            if text[:1] not in ['1', '2', '3', '4', '5']:
                wit_response = {'entities': {}}
            else:
                wit_response = wit_client.message('ela_{0} {1}'.format(text[:1], ela_questions[str(text[:1])]))
                text = ela_questions[str(text[:1])]
        if question_context_tag == 'ela_question_2':
            ela_questions = {
                "1": "Normal",
                "2": "Ligero exceso de saliva en boca, puede haber babeo nocturno",
                "3": "Exceso de saliva moderado, puede haber babeo matinal",
                "4": "Marcado exceso de saliva con algo de babeo",
                "5": "Marcado babeo, requiere constante limpieza con pañuelo",
            }
            if text[:1] not in ['1', '2', '3', '4', '5']:
                wit_response = {'entities': {}}
            else:
                wit_response = wit_client.message('ela_{0} {1}'.format(text[:1], ela_questions[str(text[:1])]))
                text = ela_questions[str(text[:1])]
        else:
            wit_response = wit_client.message(text)
        print(wit_response)
        entities = wit_response['entities'].keys()
        if 'h4h_location' in entities and 'h4h_location_context' in entities:
            graph.add_message(
                session=graph.create_session(graph.driver),
                user_id=user_id if user_id else 1,
                message=text,
                raw_data_type='location',
                raw_data_name='city',
                raw_data_value=wit_response['entities']['h4h_location'],
                debug=SERVER['debug']
            )
            callback = 'ela_question_1'
        if 'ela_speech_status' in entities and question_context_tag == 'ela_question_1':
            graph.add_message(
                session=graph.create_session(graph.driver),
                user_id=user_id if user_id else 1,
                message=text,
                raw_data_type='ela_status',
                raw_data_name='patient_status',
                raw_data_value=wit_response['entities']['ela_speech_status'][0]['value'],
                debug=SERVER['debug']
            )
            response_text = "Anoto que desde el diagnóstico tu estado de habla es: {user_data}".format(user_data=wit_response['entities']['ela_speech_status'][0]['value'])
            callback = 'ela_question_2'
        if 'ela_mouth_status' in entities and question_context_tag == 'ela_question_2':
            graph.add_message(
                session=graph.create_session(graph.driver),
                user_id=user_id if user_id else 1,
                message=text,
                raw_data_type='ela_status',
                raw_data_name='patient_status',
                raw_data_value=wit_response['entities']['ela_mouth_status'][0]['value'],
                debug=SERVER['debug']
            )
            response_text = "Anoto que desde el diagnóstico tu estado de salivación es: {user_data}".format(
                user_data=wit_response['entities']['ela_mouth_status'][0]['value'])
            callback = 'goodbye'
        if 'greetings' in entities:
            graph.add_message(
                session=graph.create_session(graph.driver),
                user_id=user_id if user_id else 1,
                message=text,
                raw_data_type='greetings',
                raw_data_name='greetings',
                raw_data_value=wit_response['entities']['greetings'][0]['value'],
                debug=SERVER['debug']
            )
            response_text = "Hola bienvenido a Eladata"
            callback = 'location_trigger'
        if question_context_tag == 'goodbye':
            response_text = "Hasta luego"
        return jsonify({
            'query': text,
            'response': response_text,
            'response_object': wit_response,
            'callback': callback
        }), 200
    return jsonify({
        'query': None,
        'response': 'Debes decirme algo'
    }), 400

@app.route('/chatbox')
def chatbox():
    return open('chat_text_box.html').read()

app.run(
    host=SERVER['host'],
    port=SERVER['port'],
    debug=SERVER['debug']
)
