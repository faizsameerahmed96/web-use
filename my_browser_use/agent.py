import os
import time

from browser_use import ActionResult, Agent, Browser
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI

from audio.record_audio import record_audio_and_transcribe
from audio.record_audio_optimize import wait_for_wakeword
from my_browser_use.custom_prompt import MySystemPrompt
import json
import asyncio
import re

profile_path = "/Users/faizahmed/Library/Application Support/Google/Chrome/Default"

controller = Controller()


# @controller.action(
#     "Ask the user for information in case you need some more information on the tasks."
# )
# def ask_human(question: str) -> str:
#     print(f"############ {question}")
#     wait_for_wakeword()
#     user_input = record_audio_and_transcribe()
#     # user_input = input(question)
#     return ActionResult(extracted_content=user_input)


async def main(message_queue):
    browser = Browser()

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
                    'window.scrollBy({ top: window.innerHeight - 100,left: 0,behavior : "smooth"})'
                )
                continue

            if "scroll up" == re.sub(r"[^A-Za-z0-9 ]+", "", task.lower()):
                page = await context.get_current_page()
                await page.evaluate(
                    'window.scrollBy({ top: -window.innerHeight - 100,left: 0,behavior : "smooth"})'
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
                    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.2),
                    # llm=ChatOpenAI(model="llama-3.2-90b-vision-preview", temperature=0.2, base_url='https://api.groq.com/openai/v1/', api_key=os.environ.get('GROQ_API_KEY')),
                    controller=controller,
                    browser=browser,
                    system_prompt_class=MySystemPrompt,
                    browser_context=context,
                )
            else:
                agent.add_new_task(task)

            result = await agent.run()
