from browser_use import ActionResult, Agent, Browser
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI

from my_browser_use.custom_prompt import MySystemPrompt

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"

controller = Controller()


@controller.action(
    "Ask the user for information in case you need some more information on the tasks."
)
def ask_human(question: str) -> str:
    answer = input(f"\n##### QUESTION: {question}\nInput: ")
    return ActionResult(extracted_content=answer)


async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        agent = None
        while True:
            task = input("Enter a task: ")
            if not agent:
                agent = Agent(
                    task=task,
                    llm=ChatOpenAI(model="gpt-4o", temperature=0.2),
                    controller=controller,
                    browser=browser,
                    system_prompt_class=MySystemPrompt,
                    browser_context=context,
                )
            else:
                agent.add_new_task(task)

            result = await agent.run()
