# Answer Generation ChatBot

Answer Generation ChatBot is a FastAPI-based chatbot designed to generate and handle questions related to product recommendations. It uses OpenAI's GPT-4 model to generate responses and SQLAlchemy to interact with a MySQL database for storing chat history.

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

## Local Usage

1. **Run the FastAPI Application:**

   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8878
   ```

   Access the API documentation at `http://0.0.0.0:8878/docs#/`


2. **Endpoints:**

   - **Root Endpoint:**
      ```sh
      curl -X GET "http://0.0.0.0:8878/"
      ```

   - **Ask Endpoint:**
     ```sh
     curl -X POST "http://0.0.0.0:8878/chatbots/ask" -H "Content-Type: application/json" -d '{
         "user_question": "Hi, I am looking for earbuds for running. They must be durable and at a good price.",
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_question": "Hi, I am looking for earbuds for climbing.",
           "user_id": "12345"
       }
       ```

     - **Example Output:**
       ```json
       {
        "status": true,
        "message": "Success",
        "data": {
          "user_question": "Hi, I am looking for earbuds for climbing.",
          "response": "These products offer distinct features, making them suitable for various needs. The Anker Soundcore Life A1 is an affordable option without many specified pros or cons. The Jabra Elite 3 stands out with aptX and good battery life but has a mediocre mic. The JLab Epic Air Sport ANC is versatile with good isolation and ANC but has touch control issues. The Jabra Elite 7 Active excels in sound quality and durability but lacks aptX support. Together, they cater to different preferences, from affordability to advanced features and durability. Choose based on your priorities. Is there anything else I can assist you with?",
          "product_ids": ["143", "146", "149","459"]
           }
         }
         ```
     
   - **Clear-Chat Endpoint:**
     ```sh
     curl -X POST "http://0.0.0.0:8878/chatbots/clear-chat" -H "Content-Type: application/json" -d '{
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_id": "12345"
       }
       ```

     - **Example Output:**
       ```json
       {
           "status": true,
           "message": "Success"
       }
       ```

   - **Chat-history Endpoint:**
     ```sh
     curl -X POST "http://0.0.0.0:8878/chatbots/chat_history" -H "Content-Type: application/json" -d '{
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_id": "12345"
       }
       ```

     - **Example Output:**
        ```json
         {
           "status": true,
           "message": "Success",
           "data": [
             {
               "question": "I need earbuds to use for climbing.",
               "answer": "These products offer distinct features, making them suitable for various needs. The Anker Soundcore Life A1 is an affordable option without many specified pros or cons. The Jabra Elite 3 stands out with aptX and good battery life but has a mediocre mic. The JLab Epic Air Sport ANC is versatile with good isolation and ANC but has touch control issues. The Jabra Elite 7 Active excels in sound quality and durability but lacks aptX support. Together, they cater to different preferences, from affordability to advanced features and durability. Choose based on your priorities. Is there anything else I can assist you with?",
               "product_ids": [
                 "143",
                 "146",
                 "149",
                 "459"
               ],
               "timestamp": "2024-09-25T00:57:37"
             }
           ]
         }
       ```


### Running on Heroku:

1. **Deploy to Heroku:**

   Follow the standard Heroku deployment process, setting up environment variables in the Heroku config as described above for the `.env` file.

2. **Heroku Environment Variables:**

   Make sure to set all necessary environment variables in your Heroku app settings:

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

3. **Access Endpoints:**

   - **Root Endpoint:**
      ```sh
      curl -X GET "https://<your-app-name>.herokuapp.com/"
      ```

   - **Ask Endpoint:**
     ```sh
     curl -X POST "https://<your-app-name>.herokuapp.com/chatbots/ask" -H "Content-Type: application/json" -d '{
         "user_question": "Hi, I am looking for earbuds for running. They must be durable and at a good price.",
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_question": "Hi, I am looking for earbuds for running. They must be durable and at a good price.",
           "user_id": "12345"
       }
       ```

     - **Example Output:**
       ```json
       {
           "status": true,
           "message": "Success",
           "data": {
               "user_question": "Hi, I am looking for earbuds for running. They must be durable and at a good price.",
               "response": "Here are some great earbuds that are durable, affordable, and ideal for running:..."
           }
       }
       ```
     
   - **Clear-Chat Endpoint:**
     ```sh
     curl -X POST "https://<your-app-name>.herokuapp.com/chatbots/clear-chat" -H "Content-Type: application/json" -d '{
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_id": "12345"
       }
       ```

     - **Example Output:**
       ```json
       {
           "status": true,
           "message": "Success"
       }
       ```

   - **Chat-history Endpoint:**
     ```sh
     curl -X POST "https://<your-app-name>.herokuapp.com/chatbots/chat_history" -H "Content-Type: application/json" -d '{
         "user_id": "12345"
     }'
     ```

     - **Example Input:**
       ```json
       {
           "user_id": "12345"
       }
       ```

     - **Example Output:**
        ```json
         {
           "status": true,
           "message": "Success",
           "data": [
             {
               "question": "I need earbuds to use for climbing.",
               "answer": "These products offer distinct features, making them suitable for various needs. The Anker Soundcore Life A1 is an affordable option without many specified pros or cons. The Jabra Elite 3 stands out with aptX and good battery life but has a mediocre mic. The JLab Epic Air Sport ANC is versatile with good isolation and ANC but has touch control issues. The Jabra Elite 7 Active excels in sound quality and durability but lacks aptX support. Together, they cater to different preferences, from affordability to advanced features and durability. Choose based on your priorities. Is there anything else I can assist you with?",
               "product_ids": [
                 "143",
                 "146",
                 "149",
                 "459"
               ],
               "timestamp": "2024-09-25T00:57:37"
             }
           ]
         }
       ```


## Project Structure

```
Answer_Generation_ChatBot/
├── api/
│   └── endpoints.py
├── core/
│   ├── bot_history_db.py
│   └── config.py
│   └── database_inspector.py
├── services/
│   ├── chatbot_service.py
│   └── db_init.py
├── .gitignore
├── README.md
├── answer_generation_chatbot.postman_collection.json
├── main.py
├── requirements.txt
└── .env
```

```markdown
   # Heroku Stack Upgrade

   This project has been upgraded from Heroku-22 to Heroku-24.

   ## Steps to Upgrade
   1. Ran the following command to upgrade the stack:
      ```sh
      heroku stack:set heroku-24 -a <your-app-name>
      ```
   2. Ensure that the application and dependencies are compatible with Heroku-24.

   Make sure to follow deployment best practices after updating the stack.
   ```
