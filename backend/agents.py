from uagents import Agent, Context, Model
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
class TestRequest(Model):
    message: str
 
class Response(Model):
    text: str

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

def calculate(expression):
    """Tool to evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})

def route_query(query):
    """Routing logic to decide if tools are needed"""
    routing_prompt = f"""
    Given the following user query, determine if any tools are needed to answer it.
    If a calculation tool is needed, respond with 'TOOL: CALCULATE'.
    If no tools are needed, respond with 'NO TOOL'.

    User query: {query}

    Response:
    """
    
    response = client.chat.completions.create(
        model=ROUTING_MODEL,
        messages=[
            {"role": "system", "content": "You are a routing assistant. Determine if the query is asking for an explanation or a query against the database."},
            {"role": "user", "content": routing_prompt}
        ],
        max_tokens=20
    )
    
    routing_decision = response.choices[0].message.content.strip()
    print('routing decision', routing_decision)
    if "TOOL: CALCULATE" in routing_decision:
        return "calculate tool needed"
    else:
        return "no tool needed"

def run_with_tool(query):
    """Use the tool model for calculation"""
    messages = [
        {"role": "system", "content": "You are a calculator assistant. Use the calculate function to perform mathematical operations and provide the results."},
        {"role": "user", "content": query}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "The mathematical expression to evaluate"}
                    },
                    "required": ["expression"]
                }
            }
        }
    ]
    response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            function_response = calculate(function_args.get("expression"))
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "calculate",
                "content": function_response,
            })
        second_response = client.chat.completions.create(
            model=TOOL_USE_MODEL,
            messages=messages
        )
        print('response', second_response.choices[0].message.content)
        return second_response.choices[0].message.content
    return response_message.content

def run_general(query):
    """Use the general model to answer the query"""
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    print('response general', response.choices[0].message.content)
    return response.choices[0].message.content

def process_query(query):
    """Process the query and route it to the appropriate model"""
    route = route_query(query)
    if route == "calculate tool needed":
        response = run_with_tool(query)
    else:
        response = run_general(query)
    
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
        # process query w groq
        response_text = process_query(_query.message)
        ctx.logger.info(f"Returning {response_text}")
        await ctx.send(sender, Response(text=response_text))
    except Exception as e:
        ctx.logger.error(f"Error occurred: {str(e)}")
        await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
    agent.run()
