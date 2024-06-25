import sqlite3
import pandas as pd
import os

class FeedzaiChallenge:
    """
    A class to handle reading CSV files, loading their contents into an SQLite database, 
    executing SQL queries, and outputting the results to a CSV file.

    Attributes:
    -----------
    database_name : str
        The name of the SQLite database to create and connect to.
    conn : sqlite3.Connection
        The SQLite connection object.
    dfs : dict
        A dictionary to hold DataFrames read from CSV files.

    Methods:
    --------
    read_csv_files(csv_files: dict):
        Reads CSV files into DataFrames and stores them in a dictionary.
    load_data(table_name: str):
        Loads a DataFrame into the SQLite database as a table.
    query_data(query: str, output_path: str):
        Executes a SQL query and writes the results to a CSV file.
    close_connection():
        Closes the SQLite database connection.
    """

    def __init__(self, database_name: str):
        """
        Constructs all the necessary attributes for the FeedzaiChallenge object.

        Parameters:
        -----------
        database_name : str
            The name of the SQLite database to create and connect to.
        """
        self.database_name = database_name
        self.conn = sqlite3.connect(f'database/{self.database_name}.db')
        self.dfs = dict()

    def read_csv_files(self, csv_files: dict):
        """
        Reads CSV files into DataFrames and stores them in a dictionary.

        Parameters:
        -----------
        csv_files : dict
            A dictionary where keys are table names and values are file paths to the CSV files.

        Raises:
        -------
        Exception
            If there is an error reading any of the CSV files.
        """
        try:
            for file in csv_files:
                self.dfs[file] = pd.read_csv(csv_files[file])
        except Exception as ex:
            print(f"Error reading file {file}: {ex}")
            raise ex

    def load_data(self, table_name: str):
        """
        Loads a DataFrame into the SQLite database as a table.

        Parameters:
        -----------
        table_name : str
            The name of the table to create in the SQLite database.

        Raises:
        -------
        Exception
            If there is an error loading data into the SQLite database.
        """
        try:
            self.dfs[table_name].to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as ex:
            print(f"Error loading data into {table_name}: {ex}")
            raise ex

    def query_data(self, query: str, output_path: str):
        """
        Executes a SQL query and writes the results to a CSV file.

        Parameters:
        -----------
        query : str
            The SQL query to execute or the path to the SQL file.
        output_path : str
            The file path where the query results will be saved as a CSV file.

        Raises:
        -------
        Exception
            If there is an error executing the query or writing the results to the CSV file.
        """
        try:
            if os.path.isfile(query):
                with open(query, 'r', encoding='utf-8') as file:
                    query_str = file.read()
            else:
                query_str = query

            result = pd.read_sql_query(query_str, self.conn)
            result.to_csv(output_path, index=False)
        except Exception as ex:
            print(f"Error executing query or writing to {output_path}: {ex}")
            raise ex

    def close_connection(self):
        """
        Closes the SQLite database connection.

        Raises:
        -------
        Exception
            If there is an error closing the database connection.
        """
        try:
            self.conn.close()
        except Exception as ex:
            print(f"Error closing conection of the database {self.database_name}: {ex}")
            raise ex

if __name__ == "__main__":

    feedzai = FeedzaiChallenge('feedzai_database')

    # .Csv files to read
    csv_files = {
    'time_off':r'csv_sources\time_off.csv',
    'work_hours':r'csv_sources\work_hours.csv'
    }

    # Reading .csv files from dictionary
    feedzai.read_csv_files(csv_files)

    # Loading tables into database
    feedzai.load_data('work_hours')
    feedzai.load_data('time_off')

    feedzai.query_data(r'queries_sql\acumulated_actual_costs.sql',r'output_files\acumulated_actual_costs.csv')
    feedzai.query_data(r'queries_sql\project_utilization.sql',r'output_files\project_utilization.csv')

    # Closing database connection
    feedzai.close_connection()