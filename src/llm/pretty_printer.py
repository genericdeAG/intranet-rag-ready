from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# this function builds the prompt for the LLM and returns the complete prompt as a string
def build_prompt(json):
    with open('src/llm/prompt.txt', 'r', encoding='utf-8') as f:
        template = f.read()
    # Convert the json dictionary to a string
    json_str = str(json)
    prompt = template.replace('{{Datei}}', json_str)
    return prompt

# this function sends the prompt to the LLM and returns the response
def gpt(website_content):
    MODEL_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    prompt = build_prompt(website_content)
    completion = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": "You are a helpful assistant cleaning up the parsed, unstructured contents of a sharepoint page in JSON format and convert it to markdown."},
        {"role": "user", "content": prompt}
    ]
    )

    response =completion.choices[0].message.content
    return response