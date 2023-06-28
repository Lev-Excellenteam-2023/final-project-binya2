import json

#     return json.dumps(response_dict, indent="\n")

#with open(f"{file_name}.json", "w") as file_out:
#         file_out.write(await chat_gpt_answer(file.PowerPointFile))
#     print("You can read the result in the json file located in the folder of the presentation.")

def make_json(text)->str:
    return json.dumps(text, indent="\n")
def writing_to_Jason_file(file_name,response_dict)->bool:
    with open(f"{file_name}.json", "w") as file_out:
        file_out.write(make_json(response_dict))
    return True
