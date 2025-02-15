from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from langchain_openai import ChatOpenAI
from playwright.sync_api import BrowserContext, sync_playwright


from my_browser_use.custom_prompt import MySystemPrompt

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"


async def main():
    browser = Browser(
        config=BrowserConfig(
            chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        )
    )
    agent = Agent(
        task="Open reddit homepage",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
    )
    result = await agent.run()
    agent.add_new_task("scroll down")
    result = await agent.run()
