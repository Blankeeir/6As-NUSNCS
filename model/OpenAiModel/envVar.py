from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv('.env.dev')

### Finetune using clear instructions:
    #https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions

##
##perform finetuning job here for model
fine_tuned_model = "gpt-4-1106-preview"



MODEL = fine_tuned_model

CLIENT = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")  # see .env
        )


SYSTEM = "When I ask for help to give me an optimal route from my current location to my destination, \
    you should reply concisely with the optimized route and their"
USER = "please provide an optimiized route with my current location delimited by the first pair of triple quotes and "
EXAMPLE = "Example: "
ASSISSTANT_INSTRUCTION = ''
TOOLS = [{"type": "code_interpreter"}
         , ]

# Code here for file upload (fine-tuning purpose)

# Code here for dynamic pricing model

# Code here for image upload




