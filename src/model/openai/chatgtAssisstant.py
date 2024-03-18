### This py implements assistant api
from openai import OpenAI
from ChatCompletion.py

client = OpenAI()
  
assistant = client.beta.assistants.create(
  name="testing assistant",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo-preview",
)

