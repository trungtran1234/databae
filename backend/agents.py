import os
import tempfile
from uagents import Agent, Context, Model, Bureau
from dotenv import load_dotenv
from db_tools import create_connection, get_all_schemas
from agent_funcs import process_query, check_query, execute_query, generate_table
from agent_class import Request, Response

load_dotenv()

query_generator_agent = Agent(
    name="Query Generator Agent",
    seed="Query Generator Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)
 
 # query generator agent displays its address and wallet address on startup
@query_generator_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {query_generator_agent.name}")
    ctx.logger.info(f"With address: {query_generator_agent.address}")
    ctx.logger.info(f"And wallet address: {query_generator_agent.wallet.address()}")

# query generator agent
# process the query and send the response to the query checker if it needs a db query
# if a query is not needed, send it back to the user
@query_generator_agent.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Request):
    user_address = sender
    ctx.logger.info(f"USER ADDRESS IN GENERATOR!! : {user_address}")
    
    ctx.logger.info("Query received")
    schema = get_all_schemas()
    try:
        # process query with Groq and database
        response = process_query(_query.query, schema)
        response_route = response['route'] # returns 'db query needed' or 'no tool needed'
        response_text = response['response'] # this is either the sql query or the response from the general model
        ctx.logger.info(f"Response: {response_text}, Sender: {sender}")

        checker_message = {
            "text": _query.query,     # User's original prompt
            "response": response_text,  # Can either be general response or SQL query from the LLM
            "sqlschema": schema            # database schema
        }

        print(checker_message)
        if response_route == "db query needed":
            ctx.logger.info(f"AYOOO: {response_text}")
            await ctx.send(QUERY_CHECKER_AGENT_ADDRESS, Response(text=checker_message['text'], query=checker_message['response'], sqlschema=checker_message['sqlschema'], user=user_address))
        else:
            await ctx.send(sender, Response(text=response_text))
        
    except Exception as e:
        ctx.logger.error(f"Error occurred: {str(e)}")
        await ctx.send(sender, Response(text="fail"))

query_checker_agent = Agent(
    name="Query Checker Agent",
    seed="Query Checker Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

QUERY_CHECKER_AGENT_ADDRESS = "agent1qfjpcvcwd2ygchzaca59wk7xmcwkdmex9teqql0zy2yrglszadvyxq6qk84"

# just some random startup function for the query checker, just displays name, address, and wallet address
@query_checker_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {query_checker_agent.name}")
    ctx.logger.info(f"With address: {query_checker_agent.address}")
    ctx.logger.info(f"And wallet address: {query_checker_agent.wallet.address()}")

# (unifinished) handle incoming queries and makes decision based on what the query checker decides
@query_checker_agent.on_message(model=Response)
async def query_handler(ctx: Context, sender: str, message: Response):
    ctx.logger.info(f"Query received from {sender}")
    userquery = message.text
    sqlquery = message.query
    schema = message.sqlschema
    user_address = message.user
    ctx.logger.info(f"USER ADDRESS in query checker!! : {user_address}")

    response = check_query(sqlquery, schema, userquery)

    ctx.logger.info(f"Response: {response}")

    if response == "QUERY CHECKER PASSED":
        await ctx.send(QUERY_EXECUTOR_AGENT_ADDRESS, Response(text=userquery, query=sqlquery, sqlschema=schema, user=user_address))
    else:
        await ctx.send(user_address, Response(text="fail"))

# query executor agent
query_executor_agent = Agent(
    name="Query Executor Agent",
    seed="Query Executor Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

QUERY_EXECUTOR_AGENT_ADDRESS = "agent1qteq8csjw7q5w8wzpevd3qk7ygrh4cra3pjnx7g2g89zlpmynmhcjkatpwd"

@query_executor_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {query_executor_agent.name}")
    ctx.logger.info(f"With address: {query_executor_agent.address}")
    ctx.logger.info(f"And wallet address: {query_executor_agent.wallet.address()}")


@query_executor_agent.on_message(model=Response)
async def query_execution(ctx: Context, sender: str, message: Response):
    response = execute_query(message.query)
    ctx.logger.info(f"Query executed: {response}")
    await ctx.send(QUERY_ANALYZER_AGENT_ADDRESS, Response(text=message.text, query=response, sqlschema=message.sqlschema, user=message.user))


# query executor agent
query_analyzer_agent = Agent(
    name="Query Analyzer Agent",
    seed="Query Analyzer Secret Phrase",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

QUERY_ANALYZER_AGENT_ADDRESS = "agent1qw9hjwe6k9tv766r265ka96504ntnmelwjc06xawqv8xzq2wsnrc7rzgkkl"

@query_analyzer_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {query_analyzer_agent.name}")
    ctx.logger.info(f"With address: {query_analyzer_agent.address}")
    ctx.logger.info(f"And wallet address: {query_analyzer_agent.wallet.address()}")

@query_analyzer_agent.on_message(model=Response)
async def query_analysis(ctx: Context, sender: str, message: Response):
    ctx.logger.info(f"Response received from {sender}")
    userquery = message.text
    sqlqueryResult = message.query
    schema = message.sqlschema
    user_address = message.user

    table = generate_table(sqlqueryResult,userquery,schema)
    print("From query analyzer:", table) #structured_data
    # Store the generated table in a temporary file
    file_path = os.path.join("response.txt")
    

    try:
        # Write the table to the response.txt file
        with open(file_path, "w") as file:
            file.write(table)
        ctx.logger.info(f"Table stored in: {file_path}")
        await ctx.send(user_address, Response(text="returned"))
        # Send a message back to the user indicating success and file location    
    except Exception as e:
        ctx.logger.error(f"Failed to write to file: {str(e)}")
    


# run all the agents at the same time basically :3 
bureau = Bureau(port=8001)
bureau.add(query_generator_agent)
bureau.add(query_checker_agent)
bureau.add(query_executor_agent)
bureau.add(query_analyzer_agent)

if __name__ == "__main__":
    bureau.run()
