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

## Usage

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
               "response": "Here are some great earbuds that are durable, affordable, and ideal for running:\n\n1. **Anker Soundcore Life A1**\n   - **Price:** $49.99\n   - **Full Overview:** These earbuds from Anker offer a secure fit, making them great for running. With good sound quality and a budget-friendly price, they are a solid choice for anyone looking to enjoy music while staying active.\n   - [Product Link](https://www.amazon.com/dp/B08KDZ2NZX?tag=at88-20&linkCode=ogi&th=1&psc=1)\n   - ![Image](https://clearbuy-cloud.nyc3.digitaloceanspaces.com/media/4232/Soundcore-by-Anker-Life-A1-True-Wireless-Earbuds.jpg)\n\n2. **Bose Sport Earbuds**\n   - **Price:** $179.00\n   - **Full Overview:** The Bose Sport Earbuds are very comfortable and make significant improvements over their predecessor, the Bose SoundSport Free. They come with a secure fit, fast charging, and good sound quality. However, they lack Bluetooth multipoint, and you need the Bose Music app to switch between devices.\n   - [Product Link](https://www.amazon.com/dp/B08CJCTG6Z?tag=at88-20&linkCode=ogi&th=1&psc=1)\n   - [Full Review](https://www.soundguys.com/bose-sport-earbuds-review-42944/)\n   - ![Image](https://clearbuy-cloud.nyc3.digitaloceanspaces.com/media/2965/Bose-Sport-Earbuds.jpg)\n\n3. **Jabra Elite 3**\n   - **Price:** $79.00\n   - **Full Overview:** The Jabra Elite 3 is an affordable option that offers support for aptX and good audio output. Pros include the price, sound quality, and battery life, but it lacks AAC support, and the microphone quality is mediocre.\n   - [Product Link](https://www.amazon.com/dp/B09B468VKX?tag=at88-20&linkCode=ogi&th=1&psc=1)\n   - [Full Review](https://www.soundguys.com/jabra-elite-3-review-59016/)\n   - ![Image](https://clearbuy-cloud.nyc3.digitaloceanspaces.com/media/5647/Jabra-Elite-3.jpg)\n\n4. **JLab Epic Air Sport ANC**\n   - **Price:** $99.00\n   - **Full Overview:** The JLab Epic Air Sport ANC is a durable, affordable, and versatile option for multifaceted individuals. Whether you're working out, on a hike, on public transit, or relaxing at home, these earbuds will be a reliable option for you.\n   - [Product Link](https://www.amazon.com/dp/B08W2FP767?tag=at88-20&linkCode=ogi&th=1&psc=1)\n   - [Full Review](https://www.soundguys.com/jlab-epic-air-sport-anc-review-74290/)\n   - ![Image](https://clearbuy-cloud.nyc3.digitaloceanspaces.com/media/3788/JLab-Epic-Air-Sport-ANC.jpg)\n\nThese earbuds are designed to stay in place and provide a secure fit, making them ideal for running.\n\n\nContinue the discussion."
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
