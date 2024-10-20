from datetime import date, datetime
import json
from db_tools import create_connection, get_all_schemas
import re
from instructions import SQL_CREATOR_INSTRUCTION, CHECKER_INSTRUCTION, DATA_ANALYSIS_INSTRUCTION
from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd


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
    EVEN IF the user's query does not directly asks for a query, they can potentially ask for Data from the table, which then you 
    can assume to answer with 'TOOL: DB_QUERY" 

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
    return groqResponse
        

def execute_query(query):
        # # Execute the extracted SQL query
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Check if results are empty
            if results:
                return json.dumps(results, cls=CustomJSONEncoder)
            else:
                return json.dumps({"message": "Query executed successfully but returned no results."})
        except Exception as e:
            return json.dumps({"error": f"SQL execution failed: {str(e)}"})

    else:
        return json.dumps({"error": "Database connection failed"})
    

def analyzer_route_tool(userquery, sqlqueryResult, schema):
    """Routing logic to let LLM decide which tools are needed"""
    messages  = [
        {
            "role": "system",
            "content": (
                "You are a data analytics assistant. You can generate charts and tables based on the provided informations. "
                f"Schema: {schema}\nSQL Query Result from the user prompt: {sqlqueryResult}"
            ),
        },
        {
            "role": "user",
            "content": userquery,
        }
    ]

    tool_definitions = [
        {
            "type": "function",
            "function": {
                "name": "generate_table",
                "description": "Generates a table based on provided data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "description": "A list of lists where the first list contains the column headers, and subsequent lists contain the rows of the table"
                        }
                    },
                    "required": ["data"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=messages,
        tools=tool_definitions,
        tool_choice="auto",
        max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    messages.append({
        "role": response_message.role,
        "content": response_message.content
    })
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        if function_name == "generate_table":
            function_response = generate_table(function_args['data'])
            tool_name = "table_gen"
            function_response_message = f"table: '{function_response}'"
        else:
            continue

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_name,
                "content": function_response_message,
            }
        )

    second_response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=messages,
        max_tokens=1024
    )
    print('response', second_response.choices[0].message.content)
    return second_response.choices[0].message.content

def generate_table(data, userquery, schema):
    """
    Generates a table using the provided columns and rows.
    
    Args:
        columns (list): A list of column headers.
        rows (list): A list of lists where each inner list represents a row.
    
    Returns:
        str: A string representation of the table (or an HTML table).
    """
    # Create a DataFrame from the provided columns and rows

    
    response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=[
            {"role": "system", "content": DATA_ANALYSIS_INSTRUCTION},
            {"role": "user", "content": f"User Query:{userquery}\n Data reference: {data}\n Schema of Database {schema}"}
        ],
        max_tokens=4096
    )
    
    #df = pd.DataFrame(response.choices[0].message.content)

    # Return the DataFrame as an HTML table or string table
    #return df.to_html(index=False)  # You can change to to_string() if text output is desired.
    json_string = response.choices[0].message.content
    print("json_string! : ", json_string)
    data = json.loads(json_string)

    df = pd.DataFrame(data)

    return df


