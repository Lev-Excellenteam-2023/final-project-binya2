import argparse
import json


def preparing_for_chat_question(file_path):

    actions = []

    return actions

async def chat_gpt_answer(file_path):
    actions = preparing_for_chat_question(file_path)
    response_dict = {}
    for index, slide_text, action in actions:
        try:
            response = await action
        except Exception as e:
            response = f"Error occurred while processing slide {index}. Error message: {str(e)}"
        response_dict[f"response {index}"] = {"text": slide_text, "response": response}
    return json.dumps(response_dict, indent="\n")  # sending the response_dict as JSON

async def main():
    user_path = argparse.ArgumentParser(description="Extract text from a PowerPoint file")
    user_path.add_argument("PowerPointFile", type=str, help="Path to the PowerPoint presentation file")
    file = user_path.parse_args()
    file_name = file.PowerPointFile.split("/")[-1].split(".")[0]
    with open(f"{file_name}.json", "w") as file_out:
        file_out.write(await chat_gpt_answer(file.PowerPointFile))
    print("You can read the result in the json file located in the folder of the presentation.")







if __name__ == "__main__":
    main()
