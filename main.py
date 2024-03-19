from web_api.dialogue_api import dialogue_api_handler
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

dialogue_api_hl = dialogue_api_handler()

parser = reqparse.RequestParser()
parser.add_argument('user_input',type=str,location='json')

def respond(res):
    return {'code':0,'message':'success','res':res}

def chat(query):
    try:
        res = dialogue_api_hl.generate_massage(query)
        return respond(res)
    except Exception as e:
        return {'code':1,'message':'fail','res':'!!! The api call is abnormal, please check the backend log'}

#print(chat("hello"))

@app.route("/ping")
def ping():
    return "Pong"

@app.route("/echo")
def echo():
    args = parser.parse_args()
    user_request_input = args['user_input']
    return respond(user_request_input)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
