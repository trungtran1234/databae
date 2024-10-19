from uagents import Agent, Context, Model
 
class TestRequest(Model):
    message: str
 
class Response(Model):
    text: str
 
# create agent instance
agent = Agent(
    name="TestAgent",
    seed="test seed",
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
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))
 

if __name__ == "__main__":
    agent.run()