from utils.file_handler import read_file
from utils.logger import get_logger
import re

logger = get_logger(__name__)


def process_md(path) -> (str, str):
    """
    Reads a Markdown (.md) file and returns the translation and purport.
    :param path: path to the Markdown file
    :return: a tuple of the translation and purport
    """
    if not path.endswith('.md'):
        logger.warning('File extension must be .md', path)
    else:
        content = read_file(path)

        try:
            if "Purport" in content:
                translation = re.findall("### Translation:(.*?)### Purport:", content, re.DOTALL)[0].strip()
                purport = re.findall("### Purport:(.*)", content, re.DOTALL)[0].strip()
            else:
                translation = re.findall("### Translation:", content, re.DOTALL)[0].strip()
                purport = ""
            return translation, purport
        except IndexError as i:
            logger.error(f"Error reading file: {path}")
