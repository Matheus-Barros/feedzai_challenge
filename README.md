# Feedzai Challenge: SQL Data Processing and Analysis

## Overview

This repository contains a Python script designed to read CSV files, load their contents into an SQLite database, execute predefined SQL queries, and output the results to CSV files. The script is aimed at providing valuable insights into the productivity and efficiency of development teams by calculating key performance indicators (KPIs) related to the work logged by team members.

## Features

- **Reading CSV Files**: Reads multiple CSV files into pandas DataFrames and stores them in a dictionary.
- **Loading Data into SQLite Database**: Loads the DataFrames into an SQLite database, creating tables as needed.
- **Executing SQL Queries**: Executes predefined SQL queries to calculate KPIs and writes the results to CSV files.
- **Handling Errors**: Comprehensive error handling to ensure robustness and reliability.
- **Closing Database Connection**: Ensures the database connection is properly closed after all operations are completed.

## Class and Methods

### FeedzaiChallenge Class

#### Attributes

- `database_name` (str): The name of the SQLite database to create and connect to.
- `conn` (sqlite3.Connection): The SQLite connection object.
- `dfs` (dict): A dictionary to hold DataFrames read from CSV files.

#### Methods

- `__init__(self, database_name: str)`: Initializes the FeedzaiChallenge object with the specified database name.
- `read_csv_files(self, csv_files: dict)`: Reads CSV files into DataFrames and stores them in a dictionary.
- `load_data(self, table_name: str)`: Loads a DataFrame into the SQLite database as a table.
- `query_data(self, query: str, output_path: str)`: Executes a SQL query and writes the results to a CSV file.
- `close_connection(self)`: Closes the SQLite database connection.

## Usage

### 1. Reading CSV Files

The `read_csv_files` method reads CSV files into pandas DataFrames. The files to be read are specified in a dictionary where the keys are the table names and the values are the file paths.

```python
csv_files = {
    'time_off': r'csv_sources/time_off.csv',
    'work_hours': r'csv_sources/work_hours.csv'
}
feedzai.read_csv_files(csv_files)
```

### 2. Loading Data into Database

The `load_data` method loads the DataFrames into the SQLite database as tables.

```python
feedzai.load_data('work_hours')
feedzai.load_data('time_off')
```

### 3. Executing SQL Queries

The `query_data` method executes predefined SQL queries to calculate KPIs and writes the results to CSV files.

```python
query_1 = """
SELECT * FROM [table_name];
"""
feedzai.query_data(query_1, r'path/file_name.csv')

```

### 4. Closing Database Connection

Ensure the database connection is closed after all operations.

```python
feedzai.close_connection()
```

## Folder Structure

The folder structure of the project is as follows:

```
feedzai_challenge
├── anaconda_environment
│   └── feedzai_challenge.yaml
├── csv_sources
│   ├── time_off.csv
│   └── work_hours.csv
├── database
│   └── feedzai_database.db
├── output_files
│   ├── acumulated_actual_costs.csv
│   └── project_utilization.csv
├── main.py
├── requirements.txt
```

### File Descriptions

- **feedzai_challenge.yaml**: Anaconda virtual env file to install.
- **main.py**: The main script containing the FeedzaiChallenge class and its methods.
- **requirements.txt**: Lists the dependencies required to run the script.
- **anaconda_environment**: Directory with virtual env used.
- **csv_sources**: Directory containing the input CSV files.
- **database**: Directory where the SQLite database is created.
- **output_files**: Directory where the output CSV files are saved.

## Setting Up the Environment - OPTION 1

To set up the environment, follow these steps:

1. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the script**:
   ```bash
   python main.py
   ```

## Setting Up the Environment with virtual env - OPTION 2

To set up the environment using Anaconda, follow these steps:

### Prerequisites

- Ensure you have Anaconda on your system.

### Steps

1. **Clone the Repository**: If you haven't already cloned the repository, do so by running the following command in your terminal:
   ```bash
   git clone https://github.com/Matheus-Barros/feedzai_challenge.git
   cd feedzai_challenge
   ```

2. **Create the Conda Environment**: Navigate to the root directory of the repository where the `feedzai_challenge.yaml` file is located. Use the following command to create a new conda environment from the provided YAML file:
   ```bash
   conda env create -f anaconda_environment/feedzai_challenge.yaml
   ```

3. **Activate the Environment**: Once the environment is created, activate it using the following command:
   ```bash
   conda activate feedzai_challenge
   ```

4. **Verify the Installation**: Ensure that the required packages are installed by checking the list of installed packages:
   ```bash
   conda list
   ```

5. **Run the Script**: With the environment activated, you can now run the main script:
   ```bash
   python main.py
   ```

## SQL Queries Explained

### Query 1: Actual Costs Calculation

This query calculates the total accumulated cost of a project at a given day by summing up all worked hours up until that day. A flat rate of $100 per work hour is used.

### Query 2: Project Utilization Calculation

This query calculates the percentage of total available hours each employee is allocated to a project, per month, assuming 8 hours/day of work time for each employee except on weekends and time off.
