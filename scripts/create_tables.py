import os
import psycopg2
from api_request import fetch_item_data, clean_item_data
from dotenv import load_dotenv

load_dotenv(dotenv_path="/opt/airflow/.env")

#Connects to the data base and returns a connection 
def connect_to_db():
    print("Connecting to PostgresQL DB...")
    print(f"Connecting as user: {os.getenv('DB_USER')}")
    print(f"To database: {os.getenv('DB_NAME')}")
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST","db"),
            port=int(os.getenv("DB_PORT", 5432)),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database failed to connect: {e}")
        raise

#Creating the table for all item details
def create_item_table(conn):
    print("Creating table if not exist...")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.rs_item_details (
                    id SERIAL PRIMARY KEY,
                    examine TEXT,
                    members TEXT,
                    lowalch INT,
                    trade_limit INT,
                    value INT,
                    highalch INT,
                    icon TEXT,
                    name TEXT,
                    inserted_at TIMESTAMP DEFAULT NOW()
                    );
            """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise


def insert_item_records(conn, data):
    """
    Inserts items using an existing database connection.
    """
    insert_query = """
        INSERT INTO dev.rs_item_details (
            id, 
            name, 
            examine, 
            members, 
            lowalch, 
            highalch, 
            value, 
            trade_limit, 
            icon
            
        )VALUES (%(id)s, %(name)s, %(examine)s, %(members)s, %(lowalch)s, %(highalch)s, %(value)s, %(limit)s, %(icon)s)
        ON CONFLICT (id) DO NOTHING;
        """
    
    # Create the cursor from the existing connection
    # We use a context manager (with) so the cursor closes automatically
    try:
        with conn.cursor() as cur:
            cur.executemany(insert_query, data)
        # Commit via the connection field
        conn.commit()
        print(f"Successfully inserted {len(data)} items.")
        
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert items: {e}")
        raise

def create_price_table(conn):
    print("Creating table if not exist...")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.prices (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    item_id INT, 
                    average_high_price INT,
                    average_low_price INT,
                    high_price_volume INT,
                    low_price_volume INT,
                    inserted_at TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise



def main():
    try:
        #Connection to postgres
        conn = connect_to_db()
        
        #Fetching the item data, cleaning it, then creating & inserting to new table
        items_data = fetch_item_data()
        cleaned_items_data = clean_item_data(items_data)
        create_item_table(conn)
        insert_item_records(conn,cleaned_items_data)

        #creating the price table
        create_price_table(conn)
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Close connection")

if __name__ == "__main__":
    main()
    


