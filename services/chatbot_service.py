import re
import logging
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain.agents.agent_types import AgentType
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from fastapi import HTTPException
from core.config import settings
from core.bot_history_db import ChatHistory

llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=settings.OPENAI_API_KEY)


def get_final_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
                **You are a helpful assistant for Clearbuy. Your primary task is to respond to user queries by generating appropriate SQL queries, executing them on the database, and formatting the results.**

                ### Instructions:
                
                ### Key Columns information to Use:
                
                - Product Columns:
                  - `id`, `category_name`, `brand_name`, `name`, `price_msrp`, `full_overview`, `pros`, `cons`.
                  
                - Usage Columns:
                  - `fit_small_ear`, `best_for_traveling`, `best_for_workout`, `best_for_work`, `best_for_music`, `best_for_gaming`, `best_for_iphone`, `best_for_samsung`, `best_for_android`.
                
                
                1. Greetings:
                   - For greetings, respond with:
                     - "Hi there, I am your helpful product recommendation assistant chatbot from Clearbuy. How may I help you today?"
                   - Do not perform any SQL operations for greetings.
                
                2. Chat History:
                   - Use past interactions to better understand the user's preferences and previous queries.
                   - Refer to previous questions and answers if relevant.
                   - Ensure continuity and context in responses.
                
                3. Product Queries:
                   - Retrieve up to four products relevant to the user's query, ensuring the category matches (e.g., Wireless Earbuds, Wireless Headphones, Wired Earbuds, Wired Headphones, etc). Correct spelling errors in product names.
                   - Summarize using key attributes and full overview table detailed information but not use columns names.
                   - Summarize using key attributes if full overview table is not available:
                   - Key Attributes Include: pros, cons, fit_small_ear, best_for_traveling, best_for_workout, best_for_work, best_for_music, best_for_gaming, best_for_iphone, best_for_samsung, best_for_android.
                   - Ensure summaries are concise, within 70 words, and written in one continuous sentence.
                   - Example summary: These four products offer distinct features, making them suitable for various needs. Product A excels in performance but is pricey. Product B offers a balanced cost and quality. Product C impresses with its advanced features yet lacks durability. Product D is budget-friendly but sacrifices some functionality. Together, they cater to different preferences, from high-end users to those seeking cost-effectiveness. Choose based on your priorities.
                   - Avoid mentioning column names directly in the response. Instead, focus on the product attributes and user value.
                   
                4. User-Centric Responses:
                   - Format responses to be user-friendly and precise.
                   - Use relevant attributes to ensure meaningful summaries.
                   - Use spelling correction for accurate results.
                
                5. Concise Summaries:
                   - Each product summary should be within 70 words.
                   - Highlight key features and critical pros and cons but don't mention their columns name in the summary.
                
                6. Clear Response Formatting:
                   - Use simple and clear language.
                   - Organize information in a user-friendly manner.
                   - Provide only requested details.
                
                7. Generate Feedback Questions:
                   - After providing the response, ask relevant feedback questions to engage the user.
                   - Instead of providing the same feedback each time, ask relevant questions to encourage user engagement.
                
                ### Responding to Product Queries:
                - Comparison Summary:
                  - Provide a 70-word combined review summarizing the top four products.
                  - Summarize using key attributes details, ensuring the summary is written in one continuous sentence. 
                  - Avoid mentioning column names directly in the response. Instead, focus on the product attributes and user value.
                   
                ### Guidelines:
                
                1. Understand the User's Query:
                   - Identify key elements and relevant database fields.
                
                2. Generate and Execute SQL Query:
                   - Write and execute a precise SQL query.
                
                3. Summarize and Format Results:
                    - Include 'Product ID:' in summaries and in the product_ids key.
                    - Summarize using key attributes, ensuring the summary is 70 words.
                    - Avoid writing attribute names in the summary except for `id`.
                    - Provide meaningful and concise summaries.
                    - Avoid mentioning these columns names in response (name, category_name, brand_name, price_msrp, full_overview, pros, cons, best_list_name, fit_small_ear, best_for_traveling, best_for_workout, best_for_work, best_for_music, best_for_gaming, best_for_iphone, best_for_samsung, best_for_android).
                    - Avoid prefacing with "Summary".  
                    - Please use the following example response for formatting reference, but ensure your response is original and not copied verbatim.  
                
                4. Utilize Chat History:
                   - Use past interactions to understand preferences.
                   - Ensure continuity and context in responses.
                   
                
                ### Example Response:
                
                **Product ID: 4322** **Product ID: 2289** **Product ID: 143** **Product ID: 146**
                
                These products offer distinct features, making them suitable for various needs. Product A excels in performance but is pricey. Product B offers a balanced cost and quality. Product C impresses with its advanced features yet lacks durability. Product D is budget-friendly but sacrifices some functionality. Together, they cater to different preferences, from high-end users to those seeking cost-effectiveness. Choose based on your priorities.
                
                
                # Last Part of response
                
                Ensure responses answer user queries directly, providing clear and concise product comparisons and summaries. 
                
                After providing the response, ask relevant feedback questions to engage the user.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}")
    ])


def extract_product_ids_and_clean_response(response_output):
    """
    Extracts all product IDs from the response and removes their mentions from the response text.

    Args:
        response_output (str): The original response containing product IDs.

    Returns:
        tuple: A tuple containing a sorted list of product IDs and the cleaned response string.
    """

    product_ids = []
    cleaned_response = response_output

    # Regular expression to match **Product ID: xxx**
    product_id_pattern = re.compile(r"\*\*Product ID:\s*(\d+)\*\*")

    # Find all product IDs
    product_ids = product_id_pattern.findall(response_output)

    # Remove all **Product ID: xxx** from the response
    cleaned_response = product_id_pattern.sub('', response_output)

    # Clean up any extra spaces or redundant line breaks resulting from removal
    cleaned_response = re.sub(r'^\s*\**Product ID:\s*\d+\**\s*', '', cleaned_response, flags=re.MULTILINE)
    cleaned_response = cleaned_response.strip()

    # Optionally, if multiple **Product ID: xxx** are present in the same line,
    # the above substitution should have removed all. However, ensure that
    # multiple spaces resulting from removal are handled.
    cleaned_response = re.sub(r'\s{2,}', ' ', cleaned_response)

    print(f"cleaned_response: {cleaned_response}")

    # Sort the product IDs numerically
    product_ids_sorted = sorted(product_ids, key=int)

    return product_ids_sorted, cleaned_response


def fetch_user_chat_history(user_id: str, db: Session, limit: int = 10):
    return db.query(ChatHistory) \
        .filter(ChatHistory.user_id == user_id) \
        .order_by(ChatHistory.created_at.desc()) \
        .limit(limit) \
        .all()


def format_chat_history_for_langchain(chat_history):
    chat_history_msgs = []
    for entry in chat_history:
        chat_history_msgs.append(HumanMessage(content=entry.question))
        chat_history_msgs.append(AIMessage(content=entry.answer))
    return chat_history_msgs


def get_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(settings.DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Yield the database session and ensure it closes after use
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_openai_response_with_langchain(user_question: str, db: Session, user_id: str):
    try:
        # Fetch the chat history for the given user
        chat_history = fetch_user_chat_history(user_id, db, limit=10)
        formatted_chat_history = format_chat_history_for_langchain(chat_history)

        sql_database = SQLDatabase.from_uri(settings.DATABASE_URI,
                                            view_support=True,
                                            schema='clearbuydb',
                                            include_tables=['SG_product_full_info_materialized'],
                                            sample_rows_in_table_info=(3))

        toolkit = SQLDatabaseToolkit(db=sql_database, llm=llm)

        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            max_iterations=30
        )

        # Prepare the final prompt using chat history
        final_prompt = get_final_prompt().format(question=user_question, chat_history=formatted_chat_history)

        # Invoke the LLM with the prompt
        response = agent_executor.invoke({"input": final_prompt})
        response_output = response.get("output", "")

        product_ids, cleaned_response = extract_product_ids_and_clean_response(response_output)

        # Save the chat history
        new_entry = ChatHistory(user_id=user_id, question=user_question, answer=cleaned_response)
        new_entry.set_product_ids(product_ids)
        db.add(new_entry)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": True,
                "message": "Success",
                "data": {
                    "user_question": user_question,
                    "response": cleaned_response,
                    "product_ids": product_ids
                }
            }
        )
    except Exception as e:
        logging.error(f"Error in get_openai_response_with_langchain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def clear_chat_history(user_id: str, db: Session):
    try:
        db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": True,
                "message": "Success",
            }
        )
    except Exception as e:
        logging.error(f"Error in clear_chat_history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error, please check the logs.")


def get_user_chat_history(user_id: str, db: Session):
    try:
        chat_history = fetch_user_chat_history(user_id, db)
        formatted_chat_history = []
        for entry in chat_history:
            formatted_chat_history.append({
                "question": entry.question,
                "answer": entry.answer,
                "product_ids": entry.get_product_ids(),
                "timestamp": entry.created_at.isoformat() if entry.created_at else None
            })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": True,
                "message": "Success",
                "data": formatted_chat_history
            }
        )
    except Exception as e:
        logging.error(f"Error in get_user_chat_history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error, please check the logs.")
