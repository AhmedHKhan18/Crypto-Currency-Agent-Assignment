from agents import Agent, Runner, function_tool
from connection import config
import requests
import chainlit as cl
import asyncio
from openai.types.responses import ResponseTextDeltaEvent


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

    result = Runner.run_streamed(
        agent, 
        input = user_input,
        run_config=config
    )

    msg = cl.Message(content="")
    await msg.send() 

    async for event in result.stream_events():
        if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
            msg.content += event.data.delta
            await msg.update()              

if __name__ == "__main__":
    asyncio.run(main())