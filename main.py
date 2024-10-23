
# Import necessary libraries
import os          # File/directory operations
import sqlite3     # Database operations
import json        # JSON handling
import gradio as gr # Web interface
from dotenv import load_dotenv  # Environment variable management
import requests    # HTTP requests

# Database Connection Function
def connect_db():
    # """
    # Creates database connection with proper error handling
    # - Creates data directory if it doesn't exist
    # - Returns SQLite connection object
    # """
    os.makedirs('data', exist_ok=True)
    db_path = os.path.abspath('data/employee.db')
    print(f"Attempting to connect to database at: {db_path}")
    return sqlite3.connect(db_path)


    
# Query Execution Function
def execute_query(sql_query):
    # """
    # Executes SQL query with comprehensive error handling
    # - Creates database connection
    # - Executes query
    # - Fetches results and column names
    # - Handles both SQLite-specific and general errors
    # - Returns tuple of (columns, results)
    # """

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return columns, result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        print(f"SQL Query: {sql_query}")
        conn.close()
        return None, {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"SQL Query: {sql_query}")
        conn.close()
        return None, {"error": str(e)}

# Gemini API interaction
def query_gemini_api(natural_query):
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        return {"error": "API key is missing. Check your .env file."}

    api_url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'
    headers = {'Content-Type': 'application/json'}
    
    # Provide context about the database schema and how to structure queries
    schema_context = """
    Database schema:
    - employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
    - departments (dept_no, dept_name)
    - dept_manager (emp_no, dept_no, from_date, to_date)
    - dept_emp (emp_no, dept_no, from_date, to_date)
    - titles (emp_no, title, from_date, to_date)
    - salaries (emp_no, salary, from_date, to_date)
    
    Important notes:
    1. Salary information is ONLY in the 'salaries' table, NOT in the 'employees' table.
    2. To get salary information, you MUST join the 'employees' and 'salaries' tables.
    3. When calculating average salary or comparing salaries, always use the 'salaries' table.
    4. For the most recent salary, use MAX(from_date) in a subquery when joining 'employees' and 'salaries'.

    Example queries:
    1. Show first 5 employees:
    SELECT e.emp_no, e.first_name, e.last_name, e.birth_date, e.gender, e.hire_date
    FROM employees e
    LIMIT 5;

    2. Get average salary of all employees:
    SELECT AVG(salary) as avg_salary
    FROM salaries;

    3. Find employees with salary above average:
    SELECT e.first_name, e.last_name, s.salary
    FROM employees e
    JOIN salaries s ON e.emp_no = s.emp_no
    WHERE s.salary > (SELECT AVG(salary) FROM salaries)
    AND s.to_date = '9999-01-01'
    LIMIT 10;

    4. Get department managers:
    SELECT e.first_name, e.last_name, d.dept_name
    FROM employees e
    JOIN dept_manager dm ON e.emp_no = dm.emp_no
    JOIN departments d ON dm.dept_no = d.dept_no
    WHERE dm.to_date = '9999-01-01'
    LIMIT 5;

    5. Find employees hired in a specific year:
    SELECT first_name, last_name, hire_date
    FROM employees
    WHERE SUBSTR(hire_date, 1, 4) = '1986'
    LIMIT 5;

    Database Schema:
    employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
    departments (dept_no, dept_name)
    dept_manager (emp_no, dept_no, from_date, to_date)
    dept_emp (emp_no, dept_no, from_date, to_date)
    titles (emp_no, title, from_date, to_date)
    salaries (emp_no, salary, from_date, to_date)
    Important Notes:
    Salary information is only available in the salaries table, not in the employees table.
    To obtain salary details, you must join the employees and salaries tables using emp_no.
    When calculating average salary or comparing salaries, always reference the salaries table.
    To find the most recent salary, use MAX(from_date) in a subquery when joining employees and salaries.
    Department information can be found in the departments, dept_manager, and dept_emp tables, and they need to be joined via dept_no and emp_no as required.
    Guidelines for Generating SQL Queries:
    Use appropriate joins and subqueries when necessary.
    When asked "who", join the relevant tables and retrieve the full name (first_name and last_name) associated with the emp_no.
    When asked "what", identify what specific information is being requested (e.g., job title, department name, salary) and join the necessary tables to retrieve that information.
    When asked "when", ensure to include relevant date fields (e.g., hire_date, from_date, to_date) and specify conditions for date ranges or specific events.
    When asked "where", determine if it relates to department assignments, employee locations, or other place-related data, and join the relevant tables.
    When asked "why", attempt to infer the reasoning based on relationships between tables, such as salary changes or departmental shifts.
    When asked "how", consider the steps or conditions involved in the query (e.g., calculating averages, retrieving maximum values).
    Additional Considerations:
    For queries involving the current department of an employee, filter based on the most recent from_date in the dept_emp table.
    For employees' current title, filter using the most recent from_date in the titles table.
    If querying for department managers, ensure the dept_manager table is joined using both emp_no and dept_no.
    
    Please follow these guidelines strictly when generating SQL queries. Ensure to use appropriate joins and subqueries when necessary.
    """
    ai_configuration = {
    "model": "gemini",  # The model name
    "temperature": 0.7,  # Controls randomness, higher values mean more randomness
    "top_k": 50,         # Limits the possible tokens at each step to the top_k most likely tokens
    "top_p": 0.9,        # Controls nucleus sampling, where 0.9 keeps the smallest possible set of tokens whose cumulative probability exceeds 90%
    "safety_settings": {
        "use_safety_filters": True,  # Enable safety filters
        "profanity_filter": True,    # Filters profanity
        "harmful_content_filter": True  # Filters harmful content
    }
    }
    
    data = {
        'contents': [
            {
                'role': 'user',
                'parts': [{'text': f"{schema_context}\n\nConvert this natural language query to SQL for the employee database: {natural_query}"}]
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        gemini_response = response.json()
        candidates = gemini_response.get('candidates', [])
        if candidates:
            sql_query = candidates[0]['content']['parts'][0]['text']
            return sql_query.strip("```sql\n").strip("```")
        else:
            return {"error": "No SQL query found in the response."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def process_query(natural_query):
    
    # """
    # Main query processing pipeline:
    # 1. Converts natural language to SQL via Gemini API
    # 2. Executes SQL query on database
    # 3. Formats results into human-readable text
    # 4. Returns dictionary with:
    #    - Original query
    #    - Generated SQL
    #    - Formatted results
    # """
    
    sql_query = query_gemini_api(natural_query)
    
    if isinstance(sql_query, dict) and "error" in sql_query:
        return sql_query
    
    columns, db_results = execute_query(sql_query)
    
    if isinstance(db_results, dict) and "error" in db_results:
        return db_results
    
    # Format the results into a human-readable response
    formatted_results = format_results(columns, db_results, natural_query)
    
    return {
        "natural_query": natural_query,
        "sql_query": sql_query,
        "results": formatted_results
    }

def format_results(columns, results, query):
    
    #   """
    # Formats database results into natural language
    # - Handles different result types (single value vs multiple rows)
    # - Constructs grammatically correct sentences
    # - Uses appropriate pronouns based on gender
    # - Combines multiple fields into coherent narratives
    # - Adds context about result limitations
    # """
    
    if columns is None or results is None:
        return "I couldn't find any results for that query."
    
    if isinstance(results, dict) and "error" in results:
        return f"I encountered an error while trying to answer that: {results['error']}"
    
    if not results:
        return "I looked, but I couldn't find any matching results for that query."
    
    formatted = "Here's what I found:\n\n"
    
    if len(results) == 1 and len(results[0]) == 1:
        # This is likely an aggregate result (e.g., AVG salary)
        value = results[0][0]
        if isinstance(value, (int, float)):
            formatted += f"The result is: {value:.2f}\n"
        else:
            formatted += f"The result is: {value}\n"
    else:
        for row in results:
            employee_info = dict(zip(columns, row))
            
            sentence = ""
            if 'first_name' in employee_info and 'last_name' in employee_info:
                sentence += f"{employee_info['first_name']} {employee_info['last_name']} "
            
            if 'birth_date' in employee_info:
                sentence += f"was born on {employee_info['birth_date']}. "
            
            if 'gender' in employee_info:
                gender_word = "He" if employee_info['gender'] == 'M' else "She"
                sentence += f"{gender_word} is {'male' if employee_info['gender'] == 'M' else 'female'}. "
            
            if 'hire_date' in employee_info:
                sentence += f"{'He' if employee_info.get('gender') == 'M' else 'She'} was hired on {employee_info['hire_date']}. "
            
            if 'salary' in employee_info:
                sentence += f"{'His' if employee_info.get('gender') == 'M' else 'Her'} salary is ${employee_info['salary']}. "
            
            if 'dept_name' in employee_info:
                sentence += f"{'He' if employee_info.get('gender') == 'M' else 'She'} works in the {employee_info['dept_name']} department. "
            
            if 'title' in employee_info:
                sentence += f"{'His' if employee_info.get('gender') == 'M' else 'Her'} job title is {employee_info['title']}. "
            
            formatted += sentence + "\n\n"
    
    if 'LIMIT' in query.upper():
        formatted += "These are just a few of the results. Let me know if you'd like to see more!"
    
    return formatted


# Gradio interface
def chatbot_interface(user_input):
    
    # """
    # Creates web interface for database interaction:
    # - Takes natural language input
    # - Returns formatted response
    # - Handles errors gracefully
    # - Maintains conversation context
    # """
    
    response = process_query(user_input)
    if isinstance(response, dict) and "error" in response:
        return f"Error: {response['error']}"
    elif isinstance(response, dict):
        return f"Query: {response['natural_query']}\n\n{response['results']}"
    else:
        return f"Unexpected response format: {response}"

# Create and launch Gradio interface
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Textbox(label="Ask about the employee database"),
    outputs=gr.Textbox(label="Response"),
    title="Employee Database AI Copilot",
    description="Ask questions about the employee database and get instant responses!"
)

if __name__ == "__main__":
    iface.launch(share=True)