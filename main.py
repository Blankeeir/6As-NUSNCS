from controller.controller import Controller
from model.OpenAiModel.count_tokens import num_tokens_from_messages
from web_api.dialogue_api import dialogue_api_handler
from flask import Flask, render_template
from flask_restful import Api, reqparse
from flask_cors import CORS
from model.OpenAiModel.envVar import *

client = CLIENT

app = Flask(__name__)
api = Api(app)
CORS(app)

MainController = Controller()
dialogue_api_hl = dialogue_api_handler()

thread1 = client.beta.threads.create()
thread2 = client.beta.threads.create()
thread3 = client.beta.threads.create()
## create several assistants for different purposes 


parser = reqparse.RequestParser()
parser.add_argument('user_input',type=str,location='json')

def respond(res):
    return {'code':0,'message':'success','res':res}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return "Pong"

@app.route("/echo")
def echo():
    args = parser.parse_args()
    user_request_input = args['user_input']
    return respond(user_request_input)

@app.route("/chat", methods=['POST'])
def chat():
    userInput = parser.parse_args()['user_input']
    if userInput:
        res = MainController.get_ai_res(userInput)
        print(res)
        return respond(res)
    return respond("No input"), 400

@app.route("/post_accident", methods=['POST'])
def post_accident():
    userInput = parser.parse_args()['user_input']
    if userInput and token_check(userInput):
        return respond(MainController.post_accident_bot_res(userInput, thread1))
    return respond("No input")

@app.route("/route_planner", methods=['POST'])
def route_planner():
    userInput = parser.parse_args()['user_input']
    if userInput and token_check(userInput):
        return respond(MainController.route_planner_res(userInput, thread2))
    return respond("No input")

@app.route("/route_info", methods=['POST'])
def route_info():
    userInput = parser.parse_args()['user_input']
    if userInput and token_check(userInput):
        return respond(MainController.route_info_res(userInput, thread3))
    return respond("No input")

def token_check(message):
    return len(message) < 4096

print(MainController.route_info_res("hi", thread3))
print(MainController.route_planner_res("hi", thread2))
print(MainController.post_accident_bot_res("hi", thread1))

if __name__ == '__main__':
    print("Starting server on port :80")
    app.run(host='0.0.0.0', port=80, debug=True)

