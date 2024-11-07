from dotenv import load_dotenv
import os
from openai import OpenAI, AzureOpenAI

load_dotenv()

def initialize_client():
    """Initialize and return the appropriate OpenAI client based on configuration."""
    use_azure = os.getenv("USE_AZURE_OPENAI", "False").lower() == "true"
    
    if use_azure:
        return AzureOpenAI(
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

def build_prompt(json):
    with open('src/llm/prompt.txt', 'r', encoding='utf-8') as f:
        template = f.read()
    # Convert the json dictionary to a string
    json_str = str(json)
    prompt = template.replace('{{Datei}}', json_str)
    return prompt

def get_model_configuration():
    """Determine the appropriate model configuration based on environment variables."""
    if os.getenv("USE_AZURE_OPENAI", "False").lower() == "true":
        return os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    
    model = os.getenv('OPENAI_MODEL_NAME')
    if os.getenv('OPENAI_MODEL_VERSION'):
        model = f"{model}-{os.getenv('OPENAI_MODEL_VERSION')}"
    return model

def create_chat_completion(client, prompt, model):
    """Handle the API request to create a chat completion."""
    return client.chat.completions.create(
        model=model,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a helpful assistant cleaning up the parsed, unstructured contents of a sharepoint page in JSON format and convert it to markdown."},
            {"role": "user", "content": prompt}
        ]
    )

def gpt(website_content):
    """Integration function that coordinates the chat completion process."""
    client = initialize_client()
    prompt = build_prompt(website_content)
    model = get_model_configuration()
    
    completion = create_chat_completion(client, prompt, model)
    return completion.choices[0].message.content