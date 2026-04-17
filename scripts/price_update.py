import os
import sys
import psycopg2
from api_request import fetch_price_data, clean_price_data
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))
#load_dotenv(dotenv_path="/opt/airflow/.env")

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



def insert_price_records(conn, data):
    """
    Inserts items using an existing database connection.
    """
    insert_query = """
        INSERT INTO dev.prices (
            item_id, 
            average_high_price,
            average_low_price,
            high_price_volume,
            low_price_volume
            
        )VALUES (%(id)s, %(avgHighPrice)s, %(avgLowPrice)s, %(highPriceVolume)s, %(lowPriceVolume)s)
        ON CONFLICT (id) DO NOTHING;
        """
    
    #Create the cursor from the existing connection
    #Uses a context manager (with) so the cursor closes automatically
    try:
        with conn.cursor() as cur:
            cur.executemany(insert_query, data)
        #Commit via the connection field
        conn.commit()
        print(f"Successfully inserted {len(data)} items.")
        
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert items: {e}")
        raise



def main():
    try:
        #Connection to postgres
        conn = connect_to_db()
        price_data = fetch_price_data()
        price_data = clean_price_data(price_data.get('data', price_data))
        insert_price_records(conn,price_data)
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Close connection")

if __name__ == "__main__":
    main()
    


