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
        os.makedirs('database', exist_ok=True)
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
            The SQL query to execute.
        output_path : str
            The file path where the query results will be saved as a CSV file.

        Raises:
        -------
        Exception
            If there is an error executing the query or writing the results to the CSV file.
        """
        try:
            result = pd.read_sql_query(query, self.conn)
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

    """
    Query 1
    Build a model using SQL to calculate “actual costs”. This indicator calculates the total accumulated cost of a 
    project at a given day by summing up all worked hours up until that day. Consider a flat rate of 100$ for the 
    cost of each work hour.
    """
    query_1 = f"""
    SELECT
        project_id,
        date,
        SUM((worked/1000.0)*100.0) OVER (PARTITION BY project_id ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_accumulated_cost
    FROM
        work_hours;
    """

    """
    Query 2

    Build a model using SQL to calculate “project utilization”. This indicator calculates the percentage of total 
    available hours each employee is allocated to a project, per month, assuming 8h/day of work time for each employee
    except on weekends and time off.
    """
    query_2 = f"""
    with max_min as (
        SELECT date from work_hours UNION SELECT date_start FROM time_off UNION SELECT date_end FROM time_off
    ),
    all_working_days as (
        with RECURSIVE DateRange AS (
            SELECT min(date) AS Date FROM max_min
            UNION ALL
            SELECT DATE(Date, '+1 day') FROM DateRange WHERE Date < (select max(date) from max_min)
        )
        SELECT Date
        FROM DateRange
        WHERE strftime('%w', Date) NOT IN ('0', '6')
    ),
    available_work_hours_per_user as (
        SELECT
            t.employee_id,
            t.employee_name,
            --t.date_start,
            --t.date_end,
            STRFTIME('%Y-%m', d.Date) as work_month,
            count(d.Date)*8 as hours
        FROM time_off t
        CROSS JOIN all_working_days d
        WHERE d.Date < t.date_start OR d.Date > t.date_end
        group by employee_id, employee_name, work_month
    ),
    worked_hours_by_month_by_project_by_employee as (
        SELECT
            wh.employee_id,
            STRFTIME('%Y-%m', wh.date) as work_month,
            wh.project_id,
            sum(wh.worked)/1000.0 as worked_total
        FROM work_hours wh
        GROUP BY employee_id, work_month, project_id
    )
    SELECT 
        ah.employee_name,
        ah.work_month,
        wh.project_id,
        100.0*wh.worked_total/ah.hours as project_utilization_percent
    FROM worked_hours_by_month_by_project_by_employee wh
    JOIN available_work_hours_per_user ah ON ah.employee_id = wh.employee_id AND ah.work_month = wh.work_month
    """

    feedzai.query_data(query_1,r'output_files\acumulated_actual_costs.csv')
    feedzai.query_data(query_2,r'output_files\project_utilization.csv')

    # Closing database connection
    feedzai.close_connection()