import os
import re
from typing import Dict, Any
from dotenv import load_dotenv
import requests

load_dotenv()


def upload_file(file_path: str, base_url: str, email: str = None) -> str:
    """
    This function uploads a file to the web app and returns the UID of the file.
    """
    url = f"{base_url}/upload"
    response = requests.post(url, files={'file': open(file_path, 'rb')}, data={'email': email})
    # response = requests.post(url, files={'file': open(file_path, 'rb')})
    if response.status_code == 200:
        response.raise_for_status()
        return response.json()['uid']
    else:
        raise Exception(f"Failed to upload file")


def get_file_status(base_url, uid=None, email=None, filename=None) -> Dict[str, Any]:
    """
    This function retrieves the status of a file from a db.    
    """
    if uid:
        url = f"{base_url}/status/"
    else:
        url = f"{base_url}/status/"

    response = requests.get(url, params={'uid': uid, 'email': email, 'filename': filename})
    if response.status_code == 200:
        response.raise_for_status()
        json_data = response.json()
        return json_data
    else:
        raise Exception(f"Failed to get file status")


def is_done(uid) -> bool:
    """
    This function returns True if the status is 'done', False otherwise.
    """
    return get_file_status(uid)['status'] == 'done'


def upload(base_url):
    file_path = input("Enter file path: ")
    email = input("Enter email or press 0 to continue without: ")
    while True:
        if not os.path.isfile(file_path):
            file_path = input("File does not exist, Enter file path: ")
            continue
        if email != '0':
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                email = input("Invalid email, Enter email or press 0 to continue without: ")
        else:
            email = None
            break
            
    return upload_file(file_path, base_url, email)


def status(base_url):
    choice = input("Enter 1 to check status by UID or 2 to check status by email and filename: ")
    while True:
        if choice == '1':
            uid = input("Enter UID: ")
            status = get_file_status(base_url, uid=uid)
            print(f"Status is {status}")
        elif choice == '2':
            email = input("Enter email: ")
            filename = input("Enter file name: ")
            status = get_file_status(base_url, email=email, filename=filename)
            print(f"Status of file {filename} is {status}")
        else:
            break
        choice = input("Enter 1 to check status by UID or 2 to check status by email and filename")


def main():
    # base_url = os.getenv("BASE_URL")
    base_url = "http://127.0.0.1:5000"
    while True:
        try:
            choice = input("Enter 1 to upload file or 2 to check status or 0 to exit:")
            if choice == '1':
                uid = upload(base_url)
                print(f"Uploaded file with UID {uid}")
            elif choice == '2':
                status(base_url)
            elif choice == '0':
                break
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
