from dotenv import load_dotenv
import os
from openai import OpenAI


def summarize_prompts(file_path):
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    with open(file_path, "r") as f:
        content = f.read()

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
        {"role": "system", "content": "You are a helpful assistant that needs to summarize the prompts given to create a single prompt that will be used to generate music with sumo ai."},
        {
            "role": "user",
            "content": f"Summarize the prompts in the file {content}. Make sure it doesn't exceed more than 2 sentences. Keep it simple and concise."
        }
    ]
    )
    sumo_ai_prompt = (completion.choices[0].message.content)
    return sumo_ai_prompt
    
summarize_prompts('prompt.txt')