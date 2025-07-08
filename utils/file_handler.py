from pathlib import Path
import os
import json


def load_json_as_dict(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def read_file(file_path):
    """
    Reads a Markdown (.md) file and returns its content as a string.

    :param file_path: Path to the .md file
    :return: String content of the file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error reading file: {e}"


def list_of_files(path: str | Path, extension: str, exclude: list[str]) -> list[str]:
    """
    Search for all files in path and return a list of all files in path with the extension appended.

    :param path: the root directory of all files
    :param extension: the file extension to search for
    :return: list of all files in path
    """

    files = []
    for root, _, files_in_dir in os.walk(path):
        for file in files_in_dir:
            if file.endswith(extension):
                for ex in exclude:
                    if ex in file:
                        break
                else:
                    files.append(os.path.join(root, file))
    return files
