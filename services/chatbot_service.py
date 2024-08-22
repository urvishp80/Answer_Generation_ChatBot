import logging
from langchain.agents.agent_types import AgentType
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi import HTTPException
from core.config import settings
from core.bot_history_db import ChatHistory

llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=settings.OPENAI_API_KEY)


def get_final_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
            You are a helpful assistant for Clearbuy. Your task is to answer user queries precisely by generating an appropriate SQL query, executing it on the database, and formatting the results.

            Instructions:
                1) If the query is a greeting like Hi, hello, "how are you?", who are you?, Good morning..etc., perform the greeting and do not perform any SQL operations. Simply respond with: "I am your product recommendation assistant chatbot".
                2) If the query is not a greeting, execute the SQL query to get the required data.
                3) Retrieve the top three product recommendations from the 'SG_only_product_full_info' view.
                4) Translate any IDs (such as category_id and brand_id) into their corresponding names.
                5) Provide answers in a human-readable sentence format.
                6) Do not list the ID in the response, only provide the associated names.
                7) Ensure recommendations are relevant to the user's query.
                8) Include the product image (image_url), product link (product_url), name (name), brand name (brand_name), price (price_msrp), along with any additional details like full review (full_overview), review URL (review_url), pros (pros), cons (cons), product rating (product_rating), and other features as per the customer's query.

            Example of a final response:

            Based on your query, here are the top three recommendations:

            1. The "iPhone 12" by Apple in the "Mobile Phones" category with a price of $799.

                [View Product](product_url)

                [Image](image_url)

                - Full Review: The iPhone 12 features a 6.1-inch display, A14 Bionic chip, and dual-camera system.
                - Review URL: [Read Reviews](review_url)
                - Pros: Excellent display, fast performance
                - Cons: Expensive
                - Product Rating: 4.5
                - Additional Features: Supports 5G, Face ID

            2. The "Galaxy S21" by Samsung in the "Mobile Phones" category with a price of $999.

                [View Product](product_url)

                [Image](image_url)

                - Full Review: The Galaxy S21 offers a 6.2-inch display, Exynos 2100, and advanced camera setup.
                - Review URL: [Read Reviews](review_url)
                - Pros: Great display, versatile camera
                - Cons: Plastic back
                - Product Rating: 4.6
                - Additional Features: 8K video recording, 120Hz refresh rate

            3. The "Pixel 5" by Google in the "Mobile Phones" category with a price of $699.

                [View Product](product_url)

                [Image](image_url)

                - Full Review: The Pixel 5 comes with a 6-inch display, Snapdragon 765G, and excellent camera software.
                - Review URL: [Read Reviews](review_url)
                - Pros: Clean software, great camera
                - Cons: Mid-range chip
                - Product Rating: 4.4
                - Additional Features: Wireless charging, water-resistant
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}")
    ])


def get_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(settings.DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_openai_response_with_langchain(user_question: str, db: Session, user_id: str):
    try:
        # Fetch the chat history for the user
        chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(
            ChatHistory.created_at).all() if user_id else []

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

        # Prepare chat history for prompting
        chat_history_msgs = []
        for entry in chat_history:
            chat_history_msgs.append(HumanMessage(content=entry.question))
            chat_history_msgs.append(AIMessage(content=entry.answer))

        # Ensure chat history is initialized
        chat_history = chat_history if 'chat_history' in locals() else []

        final_prompt = get_final_prompt()

        # response = agent_executor.invoke({
        #     "input": final_prompt.format(question=user_question)
        # })

        response = agent_executor.invoke({
            "input": final_prompt.format(question=user_question, chat_history=chat_history_msgs)
        })

        response_output = response.get("output", "")

        response_output += "\n\n\nContinue the discussion."

        # Save the chat history
        new_entry = ChatHistory(user_id=user_id, question=user_question, answer=response_output)
        db.add(new_entry)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": "Success",
                "data": {
                    "user_question": user_question,
                    "response": response_output,
                }
            }
        )
    except Exception as e:
        logging.error(f"Error in get_openai_response_with_langchain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def clear_chat_history(user_id: str, db: Session):
    db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    db.commit()
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Success",
        }
    )
