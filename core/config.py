import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# print("Loading environment variables...")

class Settings:
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOSTNAME: str = os.getenv("DATABASE_HOSTNAME")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    SSLMODE: str = os.getenv("SSLMODE")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ORGANIZATION_ID: str = os.getenv("ORGANIZATION_ID")

    @property
    def DATABASE_URI(self):
        return (f"mysql+pymysql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}")

# Instantiate the settings
settings = Settings()

required_vars = {
    'DATABASE_USERNAME': settings.DATABASE_USERNAME,
    'DATABASE_PASSWORD': settings.DATABASE_PASSWORD,
    'DATABASE_HOSTNAME': settings.DATABASE_HOSTNAME,
    'DATABASE_PORT': settings.DATABASE_PORT,
    'DATABASE_NAME': settings.DATABASE_NAME,
    'SSLMODE': settings.SSLMODE,
    'OPENAI_API_KEY': settings.OPENAI_API_KEY,
    'ORGANIZATION_ID': settings.ORGANIZATION_ID
}

# print("Loaded environment variables:")
# for var, value in required_vars.items():
#     print(f"{var}: {value}")

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
