from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from langchain_openai import ChatOpenAI
from playwright.sync_api import BrowserContext, sync_playwright
from browser_use.controller.service import Controller


from my_browser_use.custom_prompt import MySystemPrompt

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"


async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        agent = Agent(
            task="Open reddit homepage",
            llm=ChatOpenAI(model="gpt-4o-mini"),
            controller=Controller(),
            browser=browser,
            browser_context=context,
        )
        result = await agent.run()
        # agent.browser = browser
        agent.add_new_task("Scroll down")
        result = await agent.run()
