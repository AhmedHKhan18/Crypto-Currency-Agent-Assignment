from agents import Agent, Runner, function_tool
from connection import config
import requests
import chainlit as cl

@function_tool
def crypto_currency(symbol) -> str:
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}
@cl.on_message
async def main(input: cl.Message):
    user_input = input.content

    agent = Agent(
        name = 'Crypto Data Provider',
        instructions = 
        """
            You are an crypto currency data provider.your task is to provide data about all crypto currencies.
        """,
        tools = [crypto_currency]
    )

    result = await Runner.run(
        agent, 
        input = user_input,
        run_config=config
    )
    
    await cl.Message(
        content=f"{result.final_output}",
    ).send()

if __name__ == "__main__":
    main()