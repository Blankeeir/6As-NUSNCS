import requests
import json
from chatCompletion import *
from assistant import *




if __name__ == '__main__':
    requestor = ChatCompletion()
    input_s = input('user input: ')
    requestor.get_chat_response(input_s)
    '''print(res)

    response = res

    print(f"chatGPT: {response}")'''

        # To get number of tokens
        # print(num_tokens_from_messages(messages, MODEL))

