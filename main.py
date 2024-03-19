from controller.controller import Controller
from web_api.dialogue_api import dialogue_api_handler
from flask import Flask, render_template
from flask_restful import Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

MainController = Controller()
dialogue_api_hl = dialogue_api_handler()

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
    if userInput:
        return respond(MainController.post_accident_bot_res()), 200
    return respond("No input"), 400

@app.route("/route_planner", methods=['POST'])
def post_accident():
    userInput = parser.parse_args()['user_input']
    if userInput:
        return respond(MainController.route_planner_res()), 200
    return respond("No input"), 400

@app.route("/route_info", methods=['POST'])
def post_accident():
    userInput = parser.parse_args()['user_input']
    if userInput:
        return respond(MainController.route_info_res()), 200
    return respond("No input"), 400

if __name__ == '__main__':
    print("Starting server on port :80")
    app.run(host='0.0.0.0', port=80, debug=True)
