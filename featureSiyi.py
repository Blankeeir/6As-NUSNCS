import os
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI





client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("mykey")  # REPLACE WITH your api key
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)


print(chat_completion['choices'][0]['message']['content'])