# Chatbot Assistant with FastAPI and React

This project is a chatbot assistant designed for customer support, built using a FastAPI backend, React frontend, and SQLAlchemy for database interactions. The chatbot handles both normal conversational queries and database-related questions about sales and products. It generates SQL queries dynamically based on user inputs and provides human-readable summaries of the results.

## Features

- **Conversational Chatbot**: The chatbot responds to general queries with short, concise replies.
- **Database Query Generation**: For questions involving sales, products, and customers, it generates and executes SQL queries, returning a human-readable summary.
- **Chat History**: Retrieves and displays the previous chat history for a user.
- **Integration with Hugging Face LLM**: Uses a pre-trained language model to handle text processing and query generation.
- **React Frontend**: Provides an intuitive chat interface for users.

## Technologies Used

### Backend

- **FastAPI**: For building the RESTful API and handling HTTP requests.
- **SQLAlchemy**: For ORM-based database interactions.
- **MySQL**: As the relational database to store product, customer, sales, and chat history data.
- **Langchain**: For integrating the chatbot with an LLM for generating SQL queries and human-readable responses.
- **HuggingFace API**: Used for the language model endpoint.

### Frontend

- **React**: For creating the user interface.
- **Axios**: For making API requests to the backend.
- **CSS**: For styling the chat components.

## Project Structure

```bash
.
├── app/
│   ├── chat_history.py         # Handles chat history model and functions
│   ├── db.py                   # Database setup using SQLAlchemy
│   ├── llm_integration.py      # LLM integration for SQL query generation
│   ├── main.py                 # FastAPI setup and routes
│   ├── models.py               # SQLAlchemy models for customers, products, and sales
│   └── routes.py               # API endpoints for querying and fetching chat history
├── chatbot-frontend/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── components/         # Contains React components for chat functionality
│   │   └── ...
├── data/
│   ├── create_tables.sql       # SQL file for creating database tables
│   ├── insert_data.sql         # SQL file for inserting sample data
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── ...
```

## Installation

### Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **MySQL**: Make sure MySQL server is running.

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/chatbot-assistant.git
   cd chatbot-assistant
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv # for windows, "python -m venv venv"
   source venv/bin/activate # for windows, "venv\Scripts\activate.bat"
   ```

3. Install dependencies:

   ```bash
   pip3 install -r requirements.txt # for windows, "pip install -r requirements.txt"
   ```

4. Configure the `.env` file:

   ```bash
   touch .env
   ```

   Add your MySQL and HuggingFace API credentials:

   ```bash
   MYSQL_USER=<your_mysql_user>
   MYSQL_PASS=<your_mysql_password>
   MYSQL_HOST=<your_mysql_host>
   MYSQL_PORT=<your_mysql_port>
   MYSQL_DB=<your_database_name>
   HUGGINGFACEHUB_API_KEY=<your_huggingface_api_key>
   ```

5. Run the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd chatbot-frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create react build:
   ```bash
   npm run build
   mv build ../build
   ```

### Database Setup

1. Import the tables and sample data using MySQL:
   ```bash
   mysql -u <username> -p <database_name> < data/create_tables.sql
   mysql -u <username> -p <database_name> < data/insert_data.sql
   ```

## API Endpoints

### `/api/query/`

- **Method**: `POST`
- **Description**: Processes user input, generates an appropriate response (SQL or conversational), and stores the chat history.
- **Request**:
  ```json
  {
    "question": "What are the total sales for Laptops?"
  }
  ```
- **Response**:
  ```json
  {
    "response": "The total sales for Laptops are $2401."
  }
  ```

### `/api/chat-history/{user_id}`

- **Method**: `GET`
- **Description**: Retrieves chat history for a specific user.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Langchain](https://langchain.com/)
- [Hugging Face](https://huggingface.co/)
