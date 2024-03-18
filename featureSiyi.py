import os
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY")  # REPLACE WITH your api key
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gptModel",
)
