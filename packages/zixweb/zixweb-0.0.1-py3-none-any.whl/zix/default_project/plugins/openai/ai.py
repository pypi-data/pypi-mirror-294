import os
import openai

openai.api_key = os.environ.get("OPEN_AI_SECRET")
model = os.environ.get("OPEN_AI_MODEL")
system_prompt = os.getenv("OPEN_AI_SYSTEM_PROMPT", "You are a helpful assistant.")

try:
    max_tokens = int(os.environ.get("OPEN_AI_MAX_TOKENS"))
except:
    max_tokens = 1000

def completions(prompt):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        ) 
    return response["choices"][0]["message"]