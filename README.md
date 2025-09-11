
````markdown
# 🧠 Legacy Java → 🚀 Spring Boot Microservice Generator

Convert legacy Java codebases into modern Spring Boot microservices using the power of LangGraph and Azure OpenAI — with a beautiful Streamlit frontend and agentic backend.

---

## 🌟 Features

- ✅ Upload ZIP files of legacy Java code
- 🧠 Automatic code parsing and chunking
- 📝 LLM-powered JSON documentation generation
- ⚙️ Spring Boot microservice generation (Controller, Service, Model)
- 📊 Visualizes agent workflow with NetworkX + Matplotlib
- 🎨 Clean and interactive Streamlit UI

---

## 🖼️ Demo

![UI Screenshot](screenshot.png) <!-- Replace with actual screenshot path if needed -->

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.9 or higher
- An [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview) account with a deployed model (e.g., `gpt-4`)
- Environment variables set via `.env`

---

### 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/legacy-java-to-springboot.git
cd legacy-java-to-springboot

# Install dependencies
pip install -r requirements.txt
````

Or for development:

```bash
pip install -r requirements-dev.txt
```

---

### ⚙️ Setup `.env`

Create a `.env` file in the root directory:

```env
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_ENDPOINT=https://your-resource-name.openai.azure.com/
OPENAI_API_VERSION=2023-05-15
AZURE_DEPLOYMENT_NAME=your_deployment_name
```

---

### ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Developer Workflow

### 🔁 Common Tasks

```bash
make install           # Install dependencies
make install-dev       # Install dev dependencies
make lint              # Run flake8
make format            # Auto-format code with black + isort
make type-check        # Run mypy
make test              # Run tests with pytest
make run               # Launch the Streamlit app
make clean             # Remove build/test cache
```

---

## 📦 Docker Support

```bash
docker build -t legacy-springboot-app .
docker run -p 8501:8501 legacy-springboot-app
```

---

## 🧱 Tech Stack

| Layer           | Tech                                                   |
| --------------- | ------------------------------------------------------ |
| LLM Engine      | Azure OpenAI (`gpt-4`, `gpt-3.5`)                      |
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Frontend        | Streamlit                                              |
| Visualization   | NetworkX + Matplotlib                                  |
| Env Management  | python-dotenv                                          |
| Dev Tools       | Flake8, Black, Mypy, Pytest                            |

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

1. Fork the repository
2. Create your branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

---

## 📄 License

MIT License © 2025 \[Sathish Kumar]

---

## 🙏 Acknowledgements

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [OpenAI](https://openai.com/)
* [Streamlit](https://streamlit.io/)

```
