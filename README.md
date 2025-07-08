# RAG-Model-Gita

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/devsTudu/RAG-Model-Gita?utm_source=oss&utm_medium=github&utm_campaign=devsTudu%2FRAG-Model-Gita&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)


## Retrieval Augmented Generation (RAG) Model for Bhagavad Gita
This project implements a Retrieval Augmented Generation (RAG) model using Langchain, specifically tailored to provide insights and answers based on the sacred text of the Bhagavad Gita. The content of the Bhagavad Gita used in this model is sourced from the renowned publication by ISKCON (International Society for Krishna Consciousness).

The project offers multiple interfaces for interaction: a RESTful API built with FastAPI for programmatic access, and a Telegram Bot for convenient interaction directly from the messaging platform. A comprehensive `setup.py` script is also included to streamline the installation, configuration, and deployment process on your server.

## Features
* **Langchain RAG Implementation:** Leverages the power of Langchain to build an efficient RAG pipeline, enabling intelligent retrieval and generation of responses based on queries.
* **Bhagavad Gita Content:** Utilizes the authoritative text of the Bhagavad Gita from the ISKCON publication as its knowledge base.
* **FastAPI Integration:** Exposes the RAG model's capabilities via a high-performance and easy-to-use RESTful API.
* **Telegram Bot:** Provides a user-friendly interface to interact with the RAG model directly through Telegram, making it accessible on mobile devices.
* **Streamlined Setup:** Includes a setup.py script for simplified environment setup, API key configuration, testing, and server deployment.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes, or for deployment on a server.

### Prerequisites
* Python 3.9+
* pip (Python package installer)
* Postgre SQL Database for Vector Storage

## Installation
* Clone the repository
```
gh repo clone devsTudu/RAG-Model-Gita
cd RAG-Model-Gita
```

* Install dependencies:
```
pip install -r requirements.txt
```
* Setup and Deployment:
The project includes a setup.py utility to help you configure and run the application.To see all available options, 
```
python setup.py --help
```
The recommended sequence for first-time setup is:
1. **Set Variables:**
This option allows you to configure essential API keys (for Langchain, external services if any), Vector Database connection details, and your Telegram Bot Token.
```
python setup.py set-variables
```
Follow the prompts to enter your credentials.

2. **Run Tests:** After setting up your variables, it's crucial to run tests to ensure all components are correctly configured and operational. This will verify the connection to your vector database, API keys, and basic RAG functionality.

```
python setup.py test-functions
```

3. **Run Server:**
Once tests pass, you can start the FastAPI server.
```
python setup.py run_server
```
This will typically start the server on http://127.0.0.1:8000 (or a similar address), making the API accessible.

4. **Alternative Server Deployment** 

For more advanced deployment scenarios, you can deploy the FastAPI server using uvicorn directly from your terminal:

```uvicorn main:app --host 0.0.0.0 --port 8000```


Once the server is running, you can interact with the RAG model via its RESTful API, use the url for the local deployed version.

https://localhost:8000/docs

5. **Telegram Bot Deployment**

[!IMPORTANT] To handle requests from the Telegram Server, our API needs to be open for connections. And if app is deployed on local machine, it needs to open its port to public.

After hosting the API on Public Access Server,( or opening its port to public), head over to 


```
curl -X 'GET' \
  'https://<your-open-url>/telegram/setwebook?url=https%3A%2F%2F<<your-open-url>>.com%2Ftelegram%2Frespond' \

  -H 'accept: application/json'
```

## Pending Enhancment
* Increase the style of responses, into easy names like (concise/reflective/devotional/philosophical)
* Make profiles for users, (Beginner/Seeker/Scholar/Youth)
