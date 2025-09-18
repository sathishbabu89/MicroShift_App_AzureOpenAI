import os
import zipfile
import shutil
import json
import httpx

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END

# Load environment variables from .env file
load_dotenv()

# Setup HTTP client with SSL verification disabled (to avoid SSL errors)
client = httpx.Client(verify=False)

# Initialize ChatOpenAI client with environment variables
llm = ChatOpenAI(
    base_url = os.getenv("BASE_URL"),
    model = os.getenv("MODEL_NAME"),
    api_key = os.getenv("API_KEY"),
    http_client = client
)

### Step 1: Parse Legacy ZIP & Extract Java Code
def parse_legacy_code(state: dict) -> dict:
    print("Incoming state keys:", state.keys())
    zip_path = state.get("zip_path")
    if not zip_path:
        raise ValueError("zip_path is missing from the state.")
    
    extract_dir = "extracted_code"
    
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    chunks = []
    chunk_size = 1000  # number of lines per chunk

    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i in range(0, len(lines), chunk_size):
                        chunk = ''.join(lines[i:i+chunk_size])
                        chunks.append(chunk)

    state["chunks"] = chunks
    return state

### Step 2: Generate Documentation (JSON format)
def generate_documentation(state: dict) -> dict:
    chunks = state.get("chunks")
    if not chunks:
        raise ValueError("chunks are missing from the state.")

    documentation = []

    for chunk in chunks:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that generates technical documentation "
                    "from Java code. Return a JSON structure describing classes, methods, "
                    "parameters, and return types."
                )
            },
            {"role": "user", "content": chunk},
        ]

        response = llm.invoke(messages)
        documentation.append(response.content)

    state["documentation"] = json.dumps(documentation, indent=4)
    return state

### Step 3: Generate Spring Boot Microservice Code
def generate_springboot_code(state: dict) -> dict:
    documentation = state.get("documentation")
    if not documentation:
        raise ValueError("documentation is missing from the state.")

    doc_list = json.loads(documentation)

    springboot_code = []

    for doc in doc_list:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Java Spring Boot microservice generator. Given JSON documentation, "
                    "generate the entire microservice code (controller, service, models)."
                )
            },
            {"role": "user", "content": doc},
        ]

        response = llm.invoke(messages)
        springboot_code.append(response.content)

    state["springboot_code"] = "\n\n".join(springboot_code)
    return state

### LangGraph Agent Definition
def build_agent():
    builder = StateGraph(dict)

    builder.add_node("ParseLegacyCode", parse_legacy_code)
    builder.add_node("GenerateDocumentation", generate_documentation)
    builder.add_node("GenerateSpringBootCode", generate_springboot_code)

    builder.set_entry_point("ParseLegacyCode")
    builder.add_edge("ParseLegacyCode", "GenerateDocumentation")
    builder.add_edge("GenerateDocumentation", "GenerateSpringBootCode")
    builder.add_edge("GenerateSpringBootCode", END)

    return builder 
    #return builder.compile()
