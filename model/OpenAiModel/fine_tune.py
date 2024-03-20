import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict
from openai import OpenAI
from envVar import *

client = CLIENT

client.files.create(
  file=open("finetuneDataset.jsonl", "rb"),
  purpose="fine-tune"
)


















# test dataset