import requests
import os
from dotenv import load_dotenv

load_dotenv()

def query_gemini_api(natural_query):
    """Send a natural language query to the Gemini API and retrieve the generated SQL."""
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        return {"error": "API key is missing. Check your .env file."}

    api_url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [
            {
                'role': 'user',
                'parts': [{'text': natural_query}]
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Full API response
        gemini_response = response.json()
        print("Full API Response:", gemini_response)
        
        # Extract SQL query from the API response
        candidates = gemini_response.get('candidates', [])
        if candidates:
            # Assuming the SQL is embedded in the 'content' field's 'parts'
            sql_query = candidates[0]['content']['parts'][0]['text']
            # Remove any markdown formatting like ```sql
            sql_query_cleaned = sql_query.strip("```sql\n").strip("```")
            return sql_query_cleaned
        else:
            return "No SQL query found in the response."
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

#if __name__ == "__main__":
    # Test with a sample natural language query
   # test_query = "Show me all employees who joined in 2020"
    #sql_query = query_gemini_api(test_query)

    #print("Generated SQL Query:", sql_query)