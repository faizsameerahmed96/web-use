from langchain_openai import ChatOpenAI
from browser_use import Agent

async def main():
    agent = Agent(
        task="I cant buy groceries this month, are there any programs that can help me? I live in San Jose, California and I am 65 years old.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)