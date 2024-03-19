import requests
import json
from model.OpenAiModel.ChatCompletion import ChatCompletion

MODEL = "gpt-3.5-turbo"

if __name__ == '__main__':
    requestor = ChatCompletion(MODEL)

    while 1:
        input_s = input('user input: ')
        res = requestor.get_chat_response(input_s)
        print(res)

        response = res

        print(f"chatGPT: {response}")

        # To get number of tokens
        # print(num_tokens_from_messages(messages, MODEL))

