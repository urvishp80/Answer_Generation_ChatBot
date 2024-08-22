# Answer Generation ChatBot

Answer_Generation_ChatBot is a FastAPI-based chatbot designed to generate and handle questions related to product recommendations. It uses OpenAI's GPT-4 model to generate responses and SQLAlchemy to interact with a MySQL database for storing chat history.

## Features

- **Question and Answer Generation:** The chatbot can interpret user queries and provide recommendations based on SQL queries to a MySQL database.
- **Chat History Management:** Saves user queries and chatbot responses to a MySQL database for continuity and future reference.
- **User Identification:** Each user interaction is tracked by a unique user_id.

## Requirements

- Python 3.8+
- MySQL
- OpenAI API Key

## Installation

1. **Clone Repository:**

   ```sh
   git clone https://github.com/yourusername/Answer_Generation_ChatBot.git
   cd Answer_Generation_ChatBot
   ```

2. **Create and Activate Virtual Environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Environment Variables:**

   Create a `.env` file in the root directory with the following content:

   ```env
   DATABASE_USERNAME=your_database_username
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOSTNAME=your_database_hostname
   DATABASE_PORT=your_database_port
   DATABASE_NAME=clearbuydb
   SSLMODE=REQUIRED
   OPENAI_API_KEY=your_openai_api_key
   ORGANIZATION_ID=your_openai_organization_id
   ```

5. **Initialize Database:**

   Ensure you have a MySQL database running. Then, run:

   ```sh
   python services/db_init.py
   ```

## Usage

1. **Run the FastAPI Application:**

   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8878
   ```

   Access the API documentation at `http://0.0.0.0:8878/docs`

2. **Endpoints:**

   - **Root Endpoint:**
      ```sh
      curl -X GET "http://0.0.0.0:8878/"
      ```

   - **Ask Endpoint:**
      ```sh
      curl -X POST "http://0.0.0.0:8878/chatbots/ask" -H "Content-Type: application/x-www-form-urlencoded" -d "user_question=Hi i am looking for earbuds for running it must be durable and at good price&user_id=12234"
      ```

   - **Clear Chat Endpoint:**
      ```sh
      curl -X DELETE "http://0.0.0.0:8878/chatbots/clear-chat" -H "Content-Type: application/x-www-form-urlencoded" -d "user_id=12234"
      ```

## Project Structure

```
Answer_Generation_ChatBot/
├── api/
│   └── endpoints.py
├── core/
│   ├── bot_history_db.py
│   └── config.py
├── services/
│   ├── chatbot_service.py
│   └── db_init.py
├── main.py
├── requirements.txt
└── .env
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

None
```

### Description Breakdown

- **Project Title**: The title of your project.
- **Description**: A brief intro to what the project does.
- **Features**: Key features of your chatbot.
- **Requirements**: Prerequisites like Python version and necessary APIs.
- **Installation**: Steps to clone the repo, set up the environment, install dependencies, and configure the database.
- **Usage**: Instructions to run the server and use the API.
- **Project Structure**: Overview of the file and folder structure.
- **Contributing**: Invitation for contributions and instructions on how to do so.
- **License**: Licensing information of your project.
