import asyncio
import ppFile
import chatGPT
import makeJson

"""
This function gets a path to a presentation and returns a dictionary with the slide text and the response from GPT-3.
"""
async def main():
    path_file = ppFile.extract_path_from_user()
    slides_text = ppFile.extext_text_from_pp_file(path_file)
    response_dict = await chatGPT.get_chat_response(slides_text, "What is the main idea of this slide?")
    if makeJson.writing_to_Jason_file(path_file.split(".")[0], response_dict):
        print("You can read the result in the json file located in the folder of the presentation.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())  # Run the main as async function