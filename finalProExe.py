import argparse
import json


async def chat_gpt_answer(file_path):

    response_dict = {}

    return json.dumps(response_dict, indent="\n")

def main():
    user_path = argparse.ArgumentParser(description="Extract text from a PowerPoint file")
    user_path.add_argument("PowerPointFile", type=str, help="Path to the PowerPoint presentation file")
    file = user_path.parse_args()
    file_name = file.PowerPointFile.split("/")[-1].split(".")[0]








if __name__ == "__main__":
    main()
