import asyncio
import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

"""
This function gets a list of slides and a question and returns a dictionary with the slide text and the response from GPT-3.
"""


async def get_chat_response(slides_text, question) -> dict:
    response_dict = {}
    response = [None] * (len(slides_text) + 1)
    for index, slide_text in slides_text:
        response[index] = asyncio.create_task(sending_question_to_chat_gpt(slide_text, question))
    for index, slide_text in slides_text:
        res = await response[index]
        response_dict[f"response {index}"] = {"text": slide_text, "response": res}
    return response_dict


"""
This function gets a text and a question and returns the response from GPT-3.
"""


async def sending_question_to_chat_gpt(presentation_text, question) -> str:
    try:
        # Complete a chat with GPT-3
        text = presentation_text + question
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: openai.ChatCompletion.create
        (model="gpt-3.5-turbo",
         messages=[{"role": "user", "content": text}],
         timeout=100000  # seconds
         ))
        return response.choices[0].message.content
    except Exception as e:
        return f"Error occurred while processing slide. Error message: {str(e)}"
