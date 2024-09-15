# Customer Support Chatbot for Retail Analytics

This is a FastAPI-based chatbot application that integrates with an LLM (Mistral-7B-Instruct-v0.3) to generate SQL queries based on user questions and provides human-readable summaries of SQL query results. The application interacts with a MySQL database to manage chat history and handle various operations.

## Features

- **LLM Integration**: Utilizes Mistral-7B-Instruct-v0.3 to generate SQL queries and provide human-readable summaries.
- **Database Interaction**: Connects to a MySQL database to execute SQL queries and manage chat history.
- **Chat History Management**: Stores user questions, LLM-generated responses, and timestamps.

## Project Structure

- `app/main.py`: Entry point for the FastAPI application.
- `app/database.py`: Contains database setup and model definitions.
- `app/chat_history.py`: Manages chat history.
- `app/llm.py`: Handles LLM interactions for query generation and summarization.
- `app/schemas.py`: Defines Pydantic models for request and response validation.
- `requirements.txt`: Lists Python package dependencies.

## Setup

### Prerequisites

- Python 3.10+
- MySQL server
- Required Python packages

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/chatbot.git
   cd chatbot
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**

   Update `DATABASE_URL` in `app/database.py` to match your MySQL server configuration:

   ```python
   DATABASE_URL = "mysql+mysqlconnector://root:root1234@localhost:3306/chatbot"
   ```

5. **Create Database Tables**

   Run the following command to create the necessary tables:

   ```bash
   python app/database.py
   ```

### Running the Application

To start the FastAPI server, use:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### `POST /ask`

Submit a question to the chatbot and receive an answer.

**Request Body**:

```json
{
  "question": "What is the total amount of revenue generated from selling speaker?"
}
```

**Response**:

```json
{
  "answer": "The total revenue generated from selling speakers is $540.00."
}
```

### `GET /history`

Retrieve chat history.

**Response**:

```json
[
  {
    "id": 1,
    "question": "What is the total amount of revenue generated from selling speakers?",
    "answer": "The total revenue generated from selling speakers is $540.00.",
    "timestamp": "2024-09-15T12:34:56"
  }
]
```

## Code Overview

### `app/main.py`

Defines the FastAPI application and endpoints for interacting with the chatbot.

**Example**:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_response
from chat_history import add_chat_to_history, get_chat_history

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(question: Question):
    answer = generate_response(question.question)
    add_chat_to_history(question.question, answer)
    return {"answer": answer}

@app.get("/history")
def history():
    return get_chat_history()
```

### `app/database.py`

Contains the database setup and model definitions. Ensure that `create_all_tables` is called to initialize the database.

**Example**:

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:root1234@localhost:3306/chatbot"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255))
    answer = Column(Text)
    timestamp = Column(DateTime)

def create_all_tables():
    Base.metadata.create_all(bind=engine)
```

### `app/chat_history.py`

Defines the `ChatHistory` model and functions for creating and managing chat history.

**Example**:

```python
from sqlalchemy.orm import Session
from database import SessionLocal, ChatHistory
from datetime import datetime

def add_chat_to_history(question: str, answer: str):
    db: Session = SessionLocal()
    db_chat = ChatHistory(
        question=question,
        answer=answer,
        timestamp=datetime.now()
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    db.close()

def get_chat_history():
    db: Session = SessionLocal()
    chats = db.query(ChatHistory).all()
    db.close()
    return chats
```

### `app/llm.py`

Handles interaction with the LLM to generate SQL queries and convert SQL responses into human-readable summaries.

**Example**:

```python
import os
import re
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Define the HuggingFace endpoint for the LLM
sec_key = "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"
os.environ['HUGGINGFACEHUB_API_TOKEN'] = sec_key
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=sec_key)

# Define the MySQL database URI
mysql_uri = 'mysql+mysqlconnector://root:root1234@localhost:3306/chatbot'
db = SQLDatabase.from_uri(mysql_uri)

def extract_sql_from_response(response):
    sql_code = re.search(r".*(SELECT.*;).*", response, re.DOTALL)
    if sql_code:
        return sql_code.group(1).strip()
    return response.strip()

def get_schema(_):
    return "The products table has the following columns: id, name, price. The customers table has columns: id, name, email. The sales table has columns: id, product_id, customer_id, quantity, sale_date."

def run_query(query):
    return db.run(query)

query_template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:
"""
query_prompt = ChatPromptTemplate.from_template(query_template)

response_template = """Convert the SQL response to human readable summary not exceeding 2 lines.
Schema: {schema}
Question: {question}
SQL Query: {query}
SQL Response: {response}
Human-Readable Summary:
"""
response_prompt = ChatPromptTemplate.from_template(response_template)

def generate_response(question: str):
    sql_chain = (
        RunnablePassthrough.assign(schema=get_schema)
        | query_prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
        | RunnableLambda(extract_sql_from_response)
    )
    full_chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=get_schema,
            response=lambda variables: run_query(variables['query'])
        )
        | response_prompt
        | llm
    )
    response = full_chain.invoke({"question": question})
    return response
```

### `app/schemas.py`

Defines Pydantic models for validating request and response data.

**Example**:

```python
from pydantic import BaseModel

class Question(BaseModel):
    question: str

class HistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: str

    class Config:
        orm_mode = True
```

## Examples

### Generating SQL Query

For the question "What is the total amount of revenue generated from selling speakers?", the application generates the following SQL query:

```sql
SELECT SUM(quantity * price) AS total_revenue
FROM sales
JOIN products ON sales.product_id = products.id
WHERE products.name = 'speaker';
```

### Human-Readable Summary

The application converts the SQL response into a human-readable summary:

```
The total revenue generated from selling speakers is $540.00.
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```

This Markdown file includes explanations, code snippets, and examples relevant to your chatbot application. Adjust any details as needed based on your specific requirements.
```
