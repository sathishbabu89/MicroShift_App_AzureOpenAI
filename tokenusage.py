import os
import httpx
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
    http_client=client
)

def chat_with_token_usage(llm, messages):
    """
    Make a low-level chat completion request to get full response including token usage.
    """
    # Compose request payload
    payload = {
        "model": os.getenv("MODEL_NAME"),
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }

    response = client.post(
        url=os.getenv("BASE_URL") + "/v1/chat/completions",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]
    token_usage = data.get("usage", {})

    return content, token_usage

# Example usage:
messages = [{"role": "user", "content": "Write about today within 20 words"}]

content, token_usage = chat_with_token_usage(llm, messages)

print("Response Content:")
print(content)
print("\nToken Usage:")
print(token_usage)

# Your existing embeddings setup remains unchanged
embeddings = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in/",
    model='azure/genailab-maas-text-embedding-3-large',
    api_key="sk-EoakQ8NEvMzASlOPDgDTRg",
    http_client=client
)
