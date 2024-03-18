# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
import json


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))





client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("mykey")  # REPLACE WITH your api key
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",    # role: the role of the messenger (either system, user, assistant or tool)
            "content": "Say this is a test",  # user messages
        }
    ],
    model="gpt-4",
    temperature = 0.7
)


print(json.dumps(json.loads(response.model_dump_json()), indent=4))

print(response.choices[0].message.content)