import os
import time

from browser_use import ActionResult, Agent, Browser, BrowserConfig
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI

from audio.record_audio import record_audio_and_transcribe
from audio.record_audio_optimize import wait_for_wakeword
from my_browser_use.custom_prompt import MySystemPrompt
import json
import asyncio
import re

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"

controller = Controller(
    exclude_actions=["extract_content"],
)

g_message_queue = None


@controller.action(
    "ask_human - Ask the user a question or for information if required."
)
async def ask_human(question: str) -> str:
    print(f"############ {question}")
    global g_message_queue
    print(g_message_queue)
    if g_message_queue:
        await g_message_queue.put(
            json.dumps(
                {"state": "WAITING_FOR_WAKEWORD", "data": {"question": question}}
            )
        )
    wait_for_wakeword()
    user_input = record_audio_and_transcribe()
    # user_input = input(question)
    return ActionResult(extracted_content=user_input)


async def main(message_queue):
    global g_message_queue
    g_message_queue = message_queue
    browser = Browser(
        config=BrowserConfig(
            chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            disable_security=True,
        )
    )

    async with await browser.new_context() as context:
        agent = None
        while True:
            await message_queue.put(json.dumps({"state": "WAITING_FOR_WAKEWORD"}))
            wait_for_wakeword()
            await message_queue.put(json.dumps({"state": "RECORDING_AUDIO"}))
            task = record_audio_and_transcribe()

            if "scroll down" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.evaluate(
                    'window.scrollBy({ top: window.innerHeight - 20,left: 0,behavior : "smooth"})'
                )
                continue

            if "scroll down a little" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.evaluate(
                    'window.scrollBy({ top: 150,left: 0,behavior : "smooth"})'
                )
                continue

            if "scroll up a little" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.evaluate(
                    'window.scrollBy({ top: -150,left: 0,behavior : "smooth"})'
                )
                continue

            if "scroll up" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.evaluate(
                    'window.scrollBy({ top: -window.innerHeight - 20,left: 0,behavior : "smooth"})'
                )
                continue

            if "go back" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.go_back()
                continue

            print(f"Task: {task}")
            await message_queue.put(json.dumps({"state": "PERFORMING_TASK"}))
            # task = input("task: ")cl
            if not agent:
                agent = Agent(
                    task=task,
                    generate_gif=False,
                    llm=ChatOpenAI(model="gpt-4o", temperature=0.1),
                    # llm=ChatOpenAI(model="llama-3.2-90b-vision-preview", temperature=0.2, base_url='https://api.groq.com/openai/v1/', api_key=os.environ.get('GROQ_API_KEY')),
                    controller=controller,
                    planner_interval=2,
                    browser=browser,
                    system_prompt_class=MySystemPrompt,
                    browser_context=context,
                )
            else:
                agent.add_new_task(task)

            result = await agent.run()
