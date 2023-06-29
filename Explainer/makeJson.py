import json




def make_json(text) -> str:
    """
    This function gets a dictionary and returns a json string.
    """
    return json.dumps(text, indent="\n")





def writing_to_Jason_file(file_name, response_dict) -> bool:
    """
    This function gets a file name and a dictionary and writes the dictionary to a json file.
    """
    with open(f"{file_name}.json", "w") as file_out:
        file_out.write(make_json(response_dict))
    return True
