import os
from datetime import datetime
from typing import Dict, Any

from dotenv import load_dotenv
import time
import requests
load_dotenv()


def upload_file(file_path: str, base_url: str, email:str = None) -> str:
    """
    This function uploads a file to the web app and returns the UID of the file.
    """
    url = f"{base_url}/upload"
    response = requests.post(url, files={'file': open(file_path, 'rb')}, data={'email': email})
    if response.status_code == 200:
        response.raise_for_status()
        return response.json()['uid']
    else:
        raise Exception(f"Failed to upload file: {response.text}")


def get_file_status( base_url,uid = None, email=None, filename=None) -> Dict[str, Any]:
    """
    This function returns the status of a file.
    """
    url = f"{base_url}/status/{uid}"

    response = requests.post(url, params={'uid': uid, 'email': email,'filename': filename})
    response.raise_for_status()
    json_data = response.json()
    return {
        'status': json_data['status'],
        'filename': json_data['filename'],
        'timestamp': json_data['timestamp'],
        'explanation': json_data['explanation']
    }


def is_done(uid) -> bool:
    """
    This function returns True if the status is 'done', False otherwise.
    """
    return get_file_status(uid)['status'] == 'done'

def main():
    base_url = "http://127.0.0.1:5000"
    file_path = input("Enter file path: ")  # "C:\exselentim\python\final-project-binya2\file_pro\Tests.pptx"
    email = input("Enter email or press 0 to continue without: ")
    while True:

        if email != '0':
            if not '@' in email:
                email = input("Invalid email, Enter email or press 0 to continue without: ")
        else:
            email = None
        if not os.path.isfile(file_path):
            file_path = input("File does not exist, Enter file path: ")
        else:
            break
    uid = upload_file(file_path, email, base_url)
    print(f"Uploaded file {file_path} with UID {uid}")
    choice = input("Enter 1 to check status or 0 to exit: ")
    if choice == '0':
        return
    choice = input("Enter 1 to check status by UID or 2 to check status by email and filename: ")
    while True:
        if choice == '1':
            choice = input("Enter UID or press 0 to continue without: ")
            if choice != '0':
                uid = choice
            status = get_file_status(base_url, uid)
        elif choice == '2':
            choice = input("Enter email AND file name or press 0 to continue without: ")
            filename = file_path.split('\\')[-1]
            if choice != '0':
                email = input("Enter email: ")
                filename = input("Enter file name: ")
            status = get_file_status(base_url, email=email, filename=filename)
        else:
            choice = input("Invalid input, Enter 1 to check status by UID or 2 to check status by email and filename: ")

if __name__ == "__main__":
    main()
