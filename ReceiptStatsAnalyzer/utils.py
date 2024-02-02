import json, os

def load_json_folder(path : str) -> list[dict]:
    ''' Returns a list with all jsons in a folder '''
    return [json.load(open(path + file, encoding="utf-8")) for file in os.listdir(path)]

def load_all_users_receipts(path : str) -> list[dict]: 
    ''' Returns a list with all users and their receipts '''
    return {user: load_json_folder(os.path.join(path, user, "receipts/")) for user in os.listdir(path)}

def load_user_receipts(path : str) -> list[dict]:
    ''' Returns a list with all receipts of a user '''
    return load_json_folder(path + "/receipts/")

def create_user_receipts_json(path : str) -> dict:
    ''' Create a json with all receipts of a user in it's folder '''
    json.dump(load_user_receipts(path), open(os.path.join(path, "receipts.json"), "w", encoding="utf-8"), indent=4)