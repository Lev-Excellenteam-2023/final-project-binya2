import asyncio
import os
import logging
import time
import chatGPT
import makeJson
import ppFile
from dotenv import load_dotenv

load_dotenv()
UPLOADS_FOLDER = os.getenv('UPLOAD_FOLDER')
OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER')
# Configure the logger
logging.basicConfig(filename='my_logs.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create the logger object
logger = logging.getLogger('my_logger')




async def handling_file(file_path):
    """
    This function gets a path to a presentation and returns a dictionary with the slide text and the response from GPT-3.
    """
    # path_file = ppFile.extract_path_from_user()
    slides_text = ppFile.extext_text_from_pp_file(file_path)
    response_dict = await chatGPT.get_chat_response(slides_text, "What is the main idea of this slide?")
    file_path = os.path.join(OUTPUTS_FOLDER, file_path.split("\\")[-1])
    status = makeJson.writing_to_Jason_file(file_path.split(".")[0], response_dict)
    return status


def filter_files(file_list, extension, excluded_files):
    filtered_files = []
    for file in file_list:
        if file.endswith(extension) and file not in excluded_files:
            filtered_files.append(file)
    return filtered_files


async def process_file(file):
    logger.info(f"Processing file: {file} in: {time.ctime()}")
    if await handling_file(os.path.join(UPLOADS_FOLDER, file)):
        files_after_processing.append(file)
        logger.info(f"Finished processing file: {file} in: {time.ctime()}")


async def main_Explainer():
    try:
        if not os.path.exists(UPLOADS_FOLDER):
            os.makedirs(UPLOADS_FOLDER)
        if not os.path.exists(OUTPUTS_FOLDER):
            os.makedirs(OUTPUTS_FOLDER)
        files_after_processing = []
        current_time = time.time()
       while True:
        files_to_process = filter_files(os.listdir(UPLOADS_FOLDER), ".pptx", files_after_processing)
        
        for file in files_to_process:
          logger.info(f"Processing file: {file} in: {time.ctime()}")
            await process_file(file)
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Error occurred while processing file. Error message: {str(e)}")
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
        return


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main_Explainer())  # Run the main as async function
