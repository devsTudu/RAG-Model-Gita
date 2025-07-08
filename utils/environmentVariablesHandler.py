import os
from getpass import getpass
from dotenv import load_dotenv
import inquirer


from .file_handler import get_project_root, load_json_as_dict

load_dotenv()
ROOT = get_project_root()


VARIABLES = load_json_as_dict(str(ROOT / "utils" / "variables.json"))


def get(key: str) -> str:
    """Gets the secret key value, and if not exists, asks in the prompt

    Args:
        key (str): The Key whose value is being requested

    Returns:
        str : The value of the defined key
    """
    present = True
    val = str(os.getenv(key))

    while val in ["None", ""]:
        present = False
        val = getpass(f"Required {key}'s value:")
        os.environ[key] = val

    if not present:
        if os.path.exists(ROOT.joinpath(".env")):
            with open(ROOT.joinpath(".env"), "a+", encoding="utf-8") as f:
                f.write(f"\n{key}={val}\n")
                f.flush()
    return val


def checkValue(key: str, instruction: str = "This will be used in the project"):
    """
    Sets the environment value for set up.
    """
    print(key, instruction)
    try:
        value = os.environ[key]
        new_val = inquirer.password(
            f"{key} is set {value[:5]}... (leave blank to continue,"
            "or provide new one)"
        )
        if new_val == "":
            new_val = value
    except KeyError:
        new_val = inquirer.password(f"{key} is not set," "please enter a value")
    if len(new_val) < 8:
        print("Invalid Input. The Value should be atleast 8 character long")
        checkValue(key, instruction)

    os.environ[key] = new_val
