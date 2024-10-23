import os
import importlib
import json
from groq import Groq  # Assuming you're using the Groq client library
import tools

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Define models
ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

#sample data
data = [
    {
        "id": 1,
        "name": "John Doe",
        "age": 29,
        "department": "Engineering",
        "salary": 60000,
        "years_experience": 5
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "age": 34,
        "department": "Marketing",
        "salary": 70000,
        "years_experience": 8
    },
    {
        "id": 3,
        "name": "Alice Johnson",
        "age": 25,
        "department": "Sales",
        "salary": 50000,
        "years_experience": 2
    },
    {
        "id": 4,
        "name": "Robert Brown",
        "age": 45,
        "department": "HR",
        "salary": 80000,
        "years_experience": 15
    },
    {
        "id": 5,
        "name": "Emily Davis",
        "age": 30,
        "department": "Engineering",
        "salary": 65000,
        "years_experience": 6
    }
]

#to

def route_query(query):
    """Routing logic to let LLM decide if tools are needed"""
    routing_prompt = f"""
    Given the following user query, determine if any tools are needed to answer it.
    If a pie chart generation tool is needed, respond with 'TOOL: PIE_CHART'.
    If a table generation tool is needed, respond with 'TOOL: TABLE_GENERATE'.
    If a prediction tool is needed, respond with 'TOOL: PREDICT'.
    If no tools are needed, respond with 'NO TOOL'.

    User query: {query}

    Response:
    """
    
    response = client.chat.completions.create(
        model=ROUTING_MODEL,
        messages=[
            {"role": "system", "content": "You are a routing assistant. Determine if tools are needed based on the user query."},
            {"role": "user", "content": routing_prompt}
        ],
        max_tokens=1024  
    )
    
    routing_decision = response.choices[0].message.content.strip()
    
    if "TOOL: PIE_CHART" in routing_decision:
        return "pie chart tool needed"
    elif "TOOL: TABLE_GENERATE" in routing_decision:
        return "table generation tool needed"
    elif "TOOL: PREDICT" in routing_decision:
        return "predict tool needed"
    else:
        return "no tool needed"

def run_with_tool(query):
    """Use the tool use model to create the response"""
    data_json = json.dumps(data)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a data analytics assistant. You can generate charts and tables based on the provided data. "
                f"The data you can use is as follows:\n{data_json}"
            ),
        },
        {
            "role": "user",
            "content": query,
        }
    ]
    tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "generate_pie_chart",
            "description": "Generates a pie chart based on provided data",
            "parameters": {
                "type": "object",
                "properties": {
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Labels for the pie chart"
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "Values corresponding to the labels for the pie chart"
                    }
                },
                "required": ["labels", "values"]
            }
        }
    },
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
    },
    {
        "type": "function",
        "function": {
            "name": "predict_data",
            "description": "Provides a prediction based on input data using a predictive model",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "Input data for the prediction model"
                    },
                    "model": {
                        "type": "string",
                        "description": "The predictive model to use (e.g., linear regression, decision tree)"
                    }
                },
                "required": ["data", "model"]
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
    if tool_calls:
        messages.append({
            "role": response_message.role,
            "content": response_message.content
        })
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "generate_pie_chart":
                function_response = tools.generate_pie_chart(function_args['labels'], function_args['values'])
                tools.save_pie_chart(function_response)
                tool_name = "pie_chart"
                function_response_message = "Pie chart generated and saved as 'pie_chart.png'."
            elif function_name == "generate_table":
                function_response = tools.generate_table(function_args['data'])
                tool_name = "table_gen"
                function_response_message = f"table: '{function_response}'"
            elif function_name == "predict_data":
                prediction = tools.predict_data(function_args['data'], function_args['model'])
                tool_name = "predict_data"
                function_response_message = f"Prediction result: {prediction}"
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
    
    return response_message.content

def run_general(query):
    """Use the general model to answer the query since no tool is needed"""
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
    if "pie chart" in route or "table generation" in route or "predict" in route:
        response = run_with_tool(query)
    else:
        response = run_general(query)
    
    return {
        "query": query,
        "route": route,
        "response": response
    }

# Example usage
if __name__ == "__main__":
    queries = [
        "What is the capital of the Netherlands?",
        "Calculate 25 * 4 + 10",
        "Create me a pie chart of how many people are in each department",
        "Generate a table showing the name, age, and department of each employee",
        "Predict the salary of an employee with 10 years of experience using linear regression"
    ]
    
    for query in queries:
        result = process_query(query)
        print(f"Query: {result['query']}")
        print(f"Route: {result['route']}")
        print(f"Response: {result['response']}\n")