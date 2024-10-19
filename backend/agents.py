from uagents import Agent, Context, Model
from groq import Groq
import json
import os
from dotenv import load_dotenv
from db_tools import create_connection, get_all_schemas
import re
from instructions import SQL_CREATOR_INSTRUCTION
load_dotenv()

class TestRequest(Model):
    message: str

class Response(Model):
    text: str

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

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

def run_general(query, schema):
    """Use the general model to answer the query about the given schema"""
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"User query:{query}\nSchema: {schema}"}
        ]
    )
    print('response general', response.choices[0].message.content)
    return response.choices[0].message.content


def run_db_query(query):
    """Generate a SQL query based on user input and run it"""
    schemas = get_all_schemas()
    if not schemas:
        return json.dumps({"error": "Failed to retrieve schema."})
    
    # Get the raw SQL query from Groq completion API
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
            messages=[
            {"role": "system", "content": f"Here is the database schema included with all table names and columns: {schemas}"},
            {"role": "system", "content": SQL_CREATOR_INSTRUCTION},
            {"role": "user", "content": query}
        ]
    )
    
    raw_sql_query = response.choices[0].message.content.strip()

    print('raw', raw_sql_query)
    
    # Use regex to extract the SQL query from within ```sql ... ```
    match = re.search(r"```sql(.*?)```", raw_sql_query, re.DOTALL)
    if match:
        sql_query = match.group(1).strip()  
        print('query righth er', sql_query)
    else:
        print('hola')
        sql_query = raw_sql_query.strip()
    
    # Execute the extracted SQL query
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            # Check if results are empty
            if results:
                return json.dumps(results)
            else:
                return json.dumps({"message": "Query executed successfully but returned no results."})
        except Exception as e:
            return json.dumps({"error": f"SQL execution failed: {str(e)}"})

    else:
        return json.dumps({"error": "Database connection failed"})

def process_query(query, schema):
    """Process the query and route it to the appropriate model"""
    route = route_query(query)
    if route == "db query needed":
        response = run_db_query(query)
    else:
        response = run_general(query, schema)
    
    return response 

agent = Agent(
    name="Query Generator Agent",
    seed="Query Generator Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)
 
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")

# handle incoming queries
@agent.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received")
    try:
        # process query with Groq and database
        response_text = process_query(_query.message, None)  # Add schema if necessary
        ctx.logger.info(f"Response: {response_text}")
        await ctx.send(sender, Response(text=response_text))
    except Exception as e:
        ctx.logger.error(f"Error occurred: {str(e)}")
        await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
    agent.run()
