from browser_use import ActionResult, Agent, Browser
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI

from my_browser_use.custom_prompt import MySystemPrompt
from audio.record_audio import record_audio_and_transcribe

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"

controller = Controller()

@controller.action(
    "Ask the user for information in case you need some more information on the tasks."
)
def ask_human(question: str) -> str:
    print(f"############ {question}")
    user_input = record_audio_and_transcribe()
    return ActionResult(extracted_content=user_input)


async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        agent = None
        while True:
            task = record_audio_and_transcribe()
            if not agent:
                agent = Agent(
                    task=task,
                    llm=ChatOpenAI(model="gpt-4o", temperature=0.2),
                    # llm=ChatOpenAI(model="llama-3.2-90b-vision-preview", temperature=0.2, base_url='https://api.groq.com/openai/v1/'),
                    controller=controller,
                    browser=browser,
                    use_vision=False,                    
                    system_prompt_class=MySystemPrompt,
                    browser_context=context,
                )
            else:
                agent.add_new_task(task)

            result = await agent.run()
