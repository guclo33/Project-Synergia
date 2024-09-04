import os
from openai import OpenAI
import pandas as pd
import time
from openai.types import Completion, CompletionChoice, CompletionUsage




# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_text(x):
    message_content = f"considérant le modèle DISC, comment décrirait tu quelqu'un de {x}% bleu"
    response = client.chat.completions.create(messages = [
            {"role": "system", "content": "un ton professionnel, basé sur le modèle DISC"},
            {"role": "user", "content": message_content}], model= "gpt-3.5-turbo",  max_tokens = 500)
    return response
    


response= generate_text(87)

print(response.choices[0].message.content)