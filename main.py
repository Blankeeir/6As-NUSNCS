from web_api.dialogue_api import dialogue_api_handler
#from flask import Flask, render_template
#from flask_restful import Resource, Api, reqparse
#from flask_cors import CORS

dialogue_api_hl = dialogue_api_handler()

def respond(res):
    return {'code':0,'message':'success','res':res}

def chat(query):
    try:
        res = dialogue_api_hl.generate_massage(query)
        return respond(res)
    except Exception as e:
        return {'code':1,'message':'fail','res':'!!! The api call is abnormal, please check the backend log'}

print(chat("hello"))