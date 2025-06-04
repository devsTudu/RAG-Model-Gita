from utils.file_handler import get_project_root
import os
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()
ROOT = get_project_root()


def get(key:str)-> str:
    """Gets the secret key value, and if not exists, asks in the prompt

    Args:
        key (str): The Key whose value is being requested

    Returns:
        _type_: _description_
    """
    present = True
    val:str= str(os.getenv(key))
    while val in ["None", ""]:
        present = False
        val = getpass(f"Required {key}'s value:")
    os.environ[key] = val
    if not present:    
        if os.path.exists(ROOT.joinpath(".env")):
            with open(ROOT.joinpath(".env"), 'a+', encoding='utf-8') as f:
                f.write(f"\n{key}={val}\n")
    return val
