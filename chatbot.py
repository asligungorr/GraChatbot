import sqlite3
import json
from geminiapi import query_gemini_api

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect('data/employee.db')  # Ensure this path is correct

# Execute a SQL query on the SQLite database
def execute_query(sql_query):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        conn.close()
        return {"error": str(e)}


# Process the user's query and return the database results
def process_query(natural_query):
    # Use the Gemini API to convert the natural query to SQL
    sql_query = query_gemini_api(natural_query)
    
    if "error" in sql_query:
        return sql_query
    
    # Execute the generated SQL query
    db_results = execute_query(sql_query)
    
    # Return results in a structured format (JSON for now)
    return {
        "natural_query": natural_query,
        "sql_query": sql_query,
        "results": db_results
    }
