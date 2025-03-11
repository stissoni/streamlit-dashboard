import pymysql as mysql
from dotenv import load_dotenv
import os


class DBHandler:
    def __init__(self, host, port, user, password, database):
        print("Connecting to the database...")
        self.conn = mysql.connect(
            **{
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database": database,
            }
        )
        print("Connection successful!")

    def get_version(self):
        try:
            cursor = self.conn.cursor()

            # Execute the query
            cursor.execute("SELECT VERSION();")

            # Fetch the result
            result = cursor.fetchone()

            print(f"Database version: {result[0]}")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def show_tables(self):
        try:
            cursor = self.conn.cursor()

            # Execute the query
            cursor.execute("SHOW TABLES;")

            # Fetch all the results
            result = cursor.fetchall()

            # Print the result
            for row in result:
                print(row)

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def show_table_schema(self, table_name):
        try:
            cursor = self.conn.cursor()

            # Execute the query
            cursor.execute(f"DESCRIBE {table_name};")

            # Fetch all the results
            result = cursor.fetchall()

            # Print the result
            for row in result:
                print(row)

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_listings_table(self):
        try:
            cursor = self.conn.cursor()

            # Define the SQL CREATE query
            create_query = """
            CREATE TABLE listings (
                publication_id VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                manufacturer VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL,
                year INT NOT NULL,
                kilometers INT NOT NULL,
                currency VARCHAR(10) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                date DATE NOT NULL,
                PRIMARY KEY (publication_id, date)
            );
            """

            # Execute the query
            cursor.execute(create_query)

            print("Table listings created successfully!")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def drop_table(self, table_name):
        try:
            cursor = self.conn.cursor()

            # Define the SQL DROP query
            drop_query = f"DROP TABLE IF EXISTS {table_name};"

            # Execute the query
            cursor.execute(drop_query)

            print(f"Table {table_name} dropped successfully!")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def select_listings(self, manufacturer=None, model=None, date=None):
        try:
            cursor = self.conn.cursor()

            # Define the SQL SELECT query
            select_query = f"""
            SELECT
                *
            FROM
                listings
            WHERE
                manufacturer = '{manufacturer}'
                AND model = '{model}'
                AND date = '{date}';
            """

            # Execute the query
            cursor.execute(select_query)

            # Fetch all the results
            result = cursor.fetchall()

            # Print the result
            for row in result:
                print(row)

            return result

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_listings_df(self, df):
        try:
            cursor = self.conn.cursor()

            # Define the SQL INSERT query
            insert_query = """
            INSERT INTO listings (url, publication_id, title, manufacturer, model, year, kilometers, currency, price, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Convert DataFrame to list of tuples
            values = [tuple(row) for row in df.to_numpy()]

            # Execute batch insert
            cursor.executemany(insert_query, values)
            self.conn.commit()

            print(f"{cursor.rowcount} records inserted successfully!")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    # Get credentials from dotenv file
    load_dotenv(override=True)

    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    # Create a DBHandler object
    db_handler = DBHandler(host, port, user, password, database)

    # Drop the listings table
    db_handler.drop_table("listings")

    # Create the listings table
    db_handler.create_listings_table()
