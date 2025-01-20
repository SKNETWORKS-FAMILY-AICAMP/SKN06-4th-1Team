import pickle
import json
import os


def save_pickle(path: str, file_name: str, data: list):
    """
    데이터를 pickle 파일로 저장.
    """
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{file_name}", "wb") as f:
        pickle.dump(data, f)


def load_pickle(path: str) -> list:
    """
    pickle 파일에서 데이터 불러오기.
    """
    with open(path, "rb") as f:
        return pickle.load(f)


def save_json(path: str, file_name: str, data: list):
    """
    데이터를 json 파일로 저장.
    """
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{file_name}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_json(path: str) -> list:
    """
    json 파일에서 데이터 불러오기.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
