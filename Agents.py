import os
import zipfile
import shutil
import json

from openai import AzureOpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
#from langgraph.checkpoint.sqlite import SqliteSaver

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client (Azure)
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

deployment = os.getenv("AZURE_DEPLOYMENT_NAME")


### Step 1: Parse Legacy ZIP & Extract Java Code
def parse_legacy_code(state: dict) -> dict:  # Accept state as dict
    print("Incoming state keys:", state.keys())  # Debugging line to check the input state
    zip_path = state.get("zip_path")  # Safely get zip_path
    if not zip_path:
        raise ValueError("zip_path is missing from the state.")  # Handling missing key
    
    extract_dir = "extracted_code"
    
    # Clear any previous extracted code
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)

    # Extract Java files from the uploaded zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # Read and chunk Java files
    java_code = ""
    chunks = []
    chunk_size = 1000  # Define your chunk size (number of lines)

    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    java_code += ''.join(lines)
                    
                    # Split the file content into chunks
                    for i in range(0, len(lines), chunk_size):
                        chunk = ''.join(lines[i:i+chunk_size])
                        chunks.append(chunk)

    state["chunks"] = chunks  # Store the chunks in the state
    return state  # Return updated state



### Step 2: Generate Documentation (JSON format)
def generate_documentation(state: dict) -> dict:
    chunks = state.get("chunks")
    if not chunks:
        raise ValueError("chunks are missing from the state.")  # Handling missing chunks
    
    # Initialize documentation as an empty list
    documentation = []

    for chunk in chunks:
        # Prepare the LLM input for each chunk
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates technical documentation from Java code. "
                           "Return a JSON structure describing classes, methods, parameters, and return types."
            },
            {
                "role": "user",
                "content": chunk,
            },
        ]

        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.3
        )

        # Append each chunk's documentation to the list
        documentation.append(response.choices[0].message.content)
    
    # Join all chunk documentation into one JSON-like structure
    state["documentation"] = json.dumps(documentation, indent=4)  # Store final documentation as JSON
    return state  # Return updated state



### Step 3: Generate Spring Boot Microservice Code
def generate_springboot_code(state: dict) -> dict:
    documentation = state.get("documentation")
    if not documentation:
        raise ValueError("documentation is missing from the state.")  # Handling missing documentation

    # Assume documentation is a JSON list
    doc_list = json.loads(documentation)

    # Initialize Spring Boot code as an empty list
    springboot_code = []

    for doc in doc_list:
        # Prepare the LLM input for generating Spring Boot code from each chunk's documentation
        messages = [
            {
                "role": "system",
                "content": "You are a Java Spring Boot microservice generator. Given JSON documentation, "
                           "generate the entire microservice code (controller, service, models)."
            },
            {
                "role": "user",
                "content": doc,  # Each chunk's documentation
            },
        ]

        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.3
        )

        # Append generated Spring Boot code for each chunk
        springboot_code.append(response.choices[0].message.content)
    
    # Combine all generated Spring Boot code chunks
    state["springboot_code"] = "\n\n".join(springboot_code)  # Combine all chunks into final code
    return state  # Return updated state


### LangGraph Agent Definition
def build_agent():
    builder = StateGraph(dict)  # Use `dict` directly as the state type

    # Add nodes for each step
    builder.add_node("ParseLegacyCode", parse_legacy_code)
    builder.add_node("GenerateDocumentation", generate_documentation)
    builder.add_node("GenerateSpringBootCode", generate_springboot_code)

    # Define the flow of the graph (edges between nodes)
    builder.set_entry_point("ParseLegacyCode")
    builder.add_edge("ParseLegacyCode", "GenerateDocumentation")
    builder.add_edge("GenerateDocumentation", "GenerateSpringBootCode")
    builder.add_edge("GenerateSpringBootCode", END)

    # Return the compiled agent
    return builder.compile()
    
