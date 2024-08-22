from sqlalchemy import create_engine
from core.config import settings
from core.bot_history_db import Base, ChatHistory


def init_db():
    engine = create_engine(settings.DATABASE_URI)
    Base.metadata.create_all(bind=engine, tables=[ChatHistory.__table__])


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
