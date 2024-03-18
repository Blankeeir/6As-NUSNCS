import requests
import json
from ChatCompletion import ChatCompletion

if __name__ == '__main__':
    requestor = ChatCompletion("gpt-4")

    while 1:
        input_s = input('user input: ')
        res = requestor.get_chat_response(input_s)
        print(res)

        response = res

        print(f"chatGPT: {response}")

