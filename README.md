# AI Comments Assistant

AI Comments Assistant is a FastAPI-based application designed to generate comments for articles using a background task processing system with Celery. It supports asynchronous processing, user authentication via OAuth2, and a MongoDB backend for managing articles and comments.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)

---

## Features

- FastAPI for building RESTful APIs.
- Celery for background task processing.
- MongoDB and Beanie ODM for data persistence.
- LangChain with OllamaLLM for generating comments.
- Dockerized deployment.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker and Docker Compose](https://docs.docker.com/get-docker/)
- [Poetry](https://python-poetry.org/)
- [MongoDB](https://account.mongodb.com/account/login)

---

## Installation

Follow the steps below to set up the project:

---

### 1. Clone the Repository

```bash
git clone https://github.com/shkrobik2017/CommentAIAssistant.git
cd src
```

---

### 2. Configure the Environment
Create a .env file in the project root and set variables from env_example file.

---

### 3. Install Dependencies
```bash
docker-compose build
```

---

## Usage

Follow the steps below to run the project:

---

### 1. Run the application

```bash
docker-compose up
```

---

### 2. Pull ollama model to Ollama Docker Image

```bash
docker exec -it ollama ollama pull llama3.2
```

---

### 3. Access to SwaggerUI

[FastAPI - SwaggerUI](http://localhost:8000/docs)

---

