import asyncio
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

import chatGPT
import makeJson
import ppFile
from db.dbManagement import *

load_dotenv()

# UPLOADS_FOLDER = os.getenv("UPLOAD_FOLDER")
# OUTPUTS_FOLDER = os.getenv("OUTPUT_FOLDER")
UPLOADS_FOLDER = r"C:\exselentim\python\final-project-binya2\file_pro\uploads"
OUTPUTS_FOLDER = r"C:\exselentim\python\final-project-binya2\file_pro\outputs"

# Configure the logger
logging.basicConfig(filename='my_logs.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')


async def handling_file(file_path) -> bool:
    """
    This function gets a path to a presentation and returns a dictionary with the slide text and the response from GPT-3.
    """
    # path_file = ppFile.extract_path_from_user()
    slides_text = ppFile.extext_text_from_pp_file(file_path)
    response_dict = await chatGPT.get_chat_response(slides_text, "What is the main idea of this slide?")
    file_path = os.path.join(OUTPUTS_FOLDER, file_path.split("\\")[-1])
    status = makeJson.writing_to_Jason_file(file_path.split(".")[0], response_dict)
    return status


async def main_Explainer():
    try:
        while True:
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            asyncio.get_event_loop().run_until_complete(main_Explainer())
            files_before_processing = session.query(Upload).filter_by(status=Status.PENDING).all()

            for file in files_before_processing:
                file.status = Status.PROCESSING
                logger.info(f"Processing file: {file}  in: {datetime.now()}")
                if await handling_file(os.path.join(UPLOADS_FOLDER, file)):
                    file.status = Status.DONE
                    logger.info(f"Finished processing file: {file} in: {datetime.now()}")
                else:
                    file.status = Status.FAILED
                    logger.error(f"Error occurred while processing file: {file} in: {datetime.now()}")
                file.finish_time = datetime.now()
            session.close()
            await asyncio.sleep(10)
    except Exception as e:
        logger.error(f"Error occurred while processing file. Error message: {str(e)}")
        return


if __name__ == "__main__":
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)
    engine = create_engine('sqlite:///example.db')  # Run the main as async function
