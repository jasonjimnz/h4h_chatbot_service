from flask import Flask, request, jsonify
import json
from wit import Wit
from flask_cors import CORS
from config import SERVER, WIT_AI
from question_triggers import QuestionTriggers
app = Flask(__name__)
CORS(app)

wit_client = Wit(WIT_AI['API_KEY'])
wit_client.message('Hola mundo')

questions = QuestionTriggers()


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

    if (text):
        wit_response = wit_client.message(text)
        print(wit_response)
        return jsonify({
            'query': text,
            'response': 'En proceso....',
            'response_object': wit_response
        }), 200
    return jsonify({
        'query': None,
        'response': 'Debes decirme algo'
    }), 400


app.run(
    host=SERVER['host'],
    port=SERVER['port'],
    debug=SERVER['debug']
)
