from datetime import date, datetime
import json
from db_tools import create_connection, get_all_schemas
import re
from instructions import SQL_CREATOR_INSTRUCTION, CHECKER_INSTRUCTION
from groq import Groq
import os
from dotenv import load_dotenv

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# json encoder to handle the json dump when it encounters sql 
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  # Converts to 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'
        return super().default(obj)

# determines two things:
# if a db query is needed
# if a db query is not needed and only the user's query and schema are needed 
def route_query(query):
    """Routing logic to decide if tools or database queries are needed"""
    routing_prompt = f"""
    Given the following user query, determine if any tools or a database query are needed to answer it.
    If a database query is needed, respond with 'TOOL: DB_QUERY'.
    If no tools are needed, respond with 'NO TOOL'.

    User query: {query}

    Response:
    """
    
    response = client.chat.completions.create(
        model=ROUTING_MODEL,
        messages=[
            {"role": "system", "content": "You are a routing assistant. Determine if the query is asking for an explanation or a database query."},
            {"role": "user", "content": routing_prompt}
        ],
        max_tokens=20
    )
    
    routing_decision = response.choices[0].message.content.strip()
    print('routing decision', routing_decision)
    if "TOOL: DB_QUERY" in routing_decision:
        return "db query needed"
    else:
        return "no tool needed"

# if it does not need a query, run_general will be called and the LLM is only given the query and schema to make 
# an appropriate response
def run_general(query, schema):
    """Use the general model to answer the query about the given schema"""
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"User query:{query}\nSchema: {schema}"}
        ]
    )
    return response.choices[0].message.content

# generate a db query based on the user input and schemas
def create_db_query(query, schema):
    """Generate a SQL query based on user input and run it"""
    
    # Get the raw SQL query from Groq completion API
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
            messages=[
            {"role": "system", "content": f"Here is the database schema included with all table names and columns: {schema}"},
            {"role": "system", "content": SQL_CREATOR_INSTRUCTION},
            {"role": "user", "content": query}
        ]
    )
    
    raw_sql_query = response.choices[0].message.content.strip()

    
    # Use regex to extract the SQL query from within ```sql ... ```
    match = re.search(r"```sql(.*?)```", raw_sql_query, re.DOTALL)
    if match:
        sql_query = match.group(1).strip()  
    else:
        sql_query = raw_sql_query.strip()

    return raw_sql_query

# basically a helper function that creates a db query if an SQL query is needed; otherwise, it will just make
# a respones based on the user's query and schema
def process_query(query, schema):
    """Process the query and route it to the appropriate model"""
    route = route_query(query)
    if route == "db query needed":
        response = create_db_query(query, schema) # return sql, and schema
    else:
        response = run_general(query, schema)
    
    return {
        "route": route,
        "response": response 
    }
    
# this function will check if the sql is valid and send it to the appropriate agent
def check_query(sqlquery, schema, userquery):
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
        messages=[
            {"role": "system", "content": CHECKER_INSTRUCTION},
            {"role": "user", "content": f"User query:{userquery}\nSchema: {schema}\nSQL Query: {sqlquery}"}
        ]
    )

    groqResponse = response.choices[0].message.content 
    print(groqResponse)
    if groqResponse == "QUERY CHECKER FAILED":
        print(f"fail")
    elif groqResponse == "QUERY CHECKER PASSED":
        print(f"pass")
    else:
        print(f"invalid response")

    
    
