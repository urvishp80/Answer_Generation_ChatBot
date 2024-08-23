import os
import sys
sys.path.append(os.getcwd())
from sqlalchemy import create_engine, inspect
from core.config import settings


# Function to inspect the database
def inspect_database(uri):
    try:
        # Create engine
        engine = create_engine(uri)
        connection = engine.connect()
        print("Connection to the database is successful")

        # Inspect the database
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        print(f"Schemas: {schemas}")

        for schema in schemas:
            print(f"Schema: {schema}")
            table_names = inspector.get_table_names(schema="schema")
            print(f"Tables in schema '{schema}': {table_names}")

            # Fetch and print views
            views = inspector.get_view_names(schema=schema)
            print(f"Views in schema '{schema}': {views}")

        connection.close()
    except Exception as e:
        print(f"Error occurred: {e}")


# Function to inspect views in the 'clearbuydb' schema
def inspect_views(uri, schema="clearbuydb"):
    try:
        # Create engine
        engine = create_engine(uri)
        connection = engine.connect()
        print("Connection to the database is successful")

        # Inspect the database
        inspector = inspect(engine)

        # Fetch and print views
        views = inspector.get_view_names(schema=schema)
        print(f"Views in schema '{schema}': {views}")

        connection.close()
    except Exception as e:
        print(f"Error occurred: {e}")


# Function to inspect tables and their columns in the 'clearbuydb' schema
def inspect_tables_and_columns(uri, schema="clearbuydb"):
    try:
        # Create engine
        engine = create_engine(uri)
        connection = engine.connect()
        print("Connection to the database is successful")

        # Inspect the database
        inspector = inspect(engine)

        # Fetch and print table names
        table_names = inspector.get_table_names(schema=schema)
        print(f"Tables in schema '{schema}': {table_names}")

        # Loop through each table and fetch its columns
        for table_name in table_names:
            columns = inspector.get_columns(table_name, schema=schema)
            print(f"\nColumns in table '{table_name}':")
            for column in columns:
                print(f" - {column['name']} ({column['type']})")

        connection.close()
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":

    # Get the database URI from settings
    uri = settings.DATABASE_URI
    print(f"Database URI: {uri}")

    # Call the function to inspect the database
    inspect_database(uri)

    # Call the function to inspect views in the 'clearbuydb' schema
    inspect_views(uri)

    # Call the function to inspect tables and their columns in the 'clearbuydb' schema
    inspect_tables_and_columns(uri)
