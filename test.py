import requests
import json
from model.OpenAiModel.envVar import *
from model.OpenAiModel.chat_completion import *
from controller.controller import Controller


import requests
from PIL import Image
from io import BytesIO


global _test_thread
###

def modify_thread_msg(modify_thread, message_id, new_content):
    global _test_thread
    global thread1
    global thread2
    global thread3
    
    pre = f"the user modify a message. here is the new message in triple quote delimeter: '''{new_content}"
    pre += "''' please base your reply on the thread messages newly created which are history messages and provide modified answer."

    curr_thread_id = _test_thread.id
    thread_messages = client.beta.threads.messages.list(curr_thread_id)
    create_new_thread_messages(modify_thread, message_id, pre + new_content, thread_messages)


    # retrieve previous msg history
    client.beta.threads.delete(curr_thread_id)
    print(f"\n\n\ndelete {curr_thread_id}\n\n\n")






def create_new_thread_messages(modify_thread, message_id, new_content, thread_messages):
    global _test_thread
    global thread1
    global thread2
    global thread3

    new_thread_messages = []

    print(len(thread_messages.data))
    for i in range(len(thread_messages.data)):
        message = thread_messages.data[len(thread_messages.data) - i - 1]
        print(f"{message.id}       vs             {message_id}")
        if message.id != message_id:
            try:
                new_thread_messages.append({
                    "role": "user",
                    "content": message.content.text.value,
                    })
                
                print(f"append \n {message.content.text.value} \n")
            except Exception:
                print(f"error in message: {message}")

    print("\n\n\nnew\n\n\n")
    print(new_thread_messages)
    
    
    _test_thread = client.beta.threads.create(messages = new_thread_messages)
    client.beta.threads.messages.create(_test_thread.id, role="user", content = new_content)
    print(f"\n\n\nnew\n\n\n {_test_thread.id}")
    
    print(_test_thread)
    print(client.beta.threads.messages.list(_test_thread.id))




# def test_image_generation(prompt_history):
#     image_url = Controller.get_ai_image_url(prompt_history)  # Replace with your image URL
#     response = requests.get(image_url)
#     if response.status_code == 200:
#         image_data = response.content
#         image = Image.open(BytesIO(image_data))
#         image.show()  # Display the image
#         return "Image displayed successfully"
#     else:
#         return "Failed to retrieve image"



# requestor = ChatCompletion()
# input_s = input('user input: ')
# requestor.get_chat_response(input_s)

# test thread modification
if __name__ == '__main__':
    # requestor = ChatCompletion()
    # input_s = input('user input: ')
    # res = requestor.get_chat_response(input_s)
    # print(res)
    # modify_thread_msg(1, 1, "I need to solve the equation `3x + 11 = 14`. Can you help me?")
    # print(client.beta.threads.messages.list(_test_thread.id))
    # print(test_image_generation("I need to solve the equation `3x + 11 = 14`. Can you help me?"))
    client = CLIENT
    _test_thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id= _test_thread.id,
        role="user",
        content= "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    )

    message2 = client.beta.threads.messages.create(
        thread_id= _test_thread.id,
        role="user",
        content= "please provide detailed mathematical solution and explanation."
    )

    ## modify content
    modified_prompt = input("user input: ")
    modify_thread_msg(0, message.id, modified_prompt)

    print(f"\n\n new thread \n\n\n{_test_thread.id}")
    print(client.beta.threads.messages.list(_test_thread.id))

    

'''print(res)

response = res

print(f"chatGPT: {response}")'''

    # To get number of tokens
    # print(num_tokens_from_messages(messages, MODEL))

