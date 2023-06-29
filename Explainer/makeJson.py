import json

"""
This function gets a dictionary and returns a json string.
"""


def make_json(text) -> str:
    return json.dumps(text, indent="\n")


"""
This function gets a file name and a dictionary and writes the dictionary to a json file.
"""


def writing_to_Jason_file(file_name, response_dict) -> bool:
    with open(f"{file_name}.json", "w") as file_out:
        file_out.write(make_json(response_dict))
    return True
