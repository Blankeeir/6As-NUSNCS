import openai
import os
os.environ["OPENAI_API_KEY"] = ""



response = openai.ChatCompletion.create(
  model="gpt-4-general",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]
)

print(response['choices'][0]['message']['content'])