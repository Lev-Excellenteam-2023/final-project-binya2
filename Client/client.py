import os
from datetime import datetime
from typing import Dict, Any

from dotenv import load_dotenv
import time
import requests
load_dotenv()


def upload_file(file_path: str, base_url: str) -> str:
    """
    This function uploads a file to the web app and returns the UID of the file.
    """
    url = f"{base_url}/upload"
    response = requests.post(url, files={'file': open(file_path, 'rb')})
    response.raise_for_status()
    json_data = response.json()
    return json_data['uid']

def get_file_status(uid, base_url):
    """
    This function returns the status of a file.
    """
    url = f"{base_url}/status/{uid}"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()

    status = json_data['status']
    filename = json_data['filename']
    timestamp = json_data['timestamp']
    explanation = json_data['explanation']
    return {
        'status': status,
        'filename': filename,
        'timestamp': timestamp,
        'explanation': explanation
    }


def is_done(status) -> bool:
    """
    This function returns True if the status is 'done', False otherwise.
    """
    return status['status'] == 'done'


if __name__ == "__main__":
    base_url = r"http://127.0.0.1:5000"
    file_path = r"C:\exselentim\python\final-project-binya2\Tests.pptx"
    uid = upload_file(file_path, base_url)
    while True:
        status = get_file_status(uid, base_url)
        if is_done(status):
            print(f"Done! Explanation: {status['explanation']}")
            break
        else:
            print(f"Waiting for file {status['filename']}...")
            time.sleep(5)