from agents import Agent, Runner, function_tool
from connection import config
import requests

@function_tool
def crypto_currency() -> str:
    url = 'https://api.binance.com/api/v3/ticker/price?symbol={currency}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}

agent = Agent(
    name = 'Current Data',
    instructions = 
    """
        You are an helpful assistant. Your task is to
        help user with its queries.
    """,
    tools = [crypto_currency]
)

result = Runner.run_sync(
    agent, 
    input = 'can you convert BTCUSDT',
    run_config=config
)

print(result.final_output)