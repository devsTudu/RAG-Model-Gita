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
            if  "Translation" not in content:
                logger.warning(f"Translation section not found in {path}")
                return "", content
            elif "Purport" in content:
                translation = re.findall("### Translation:(.*?)### Purport:", content, re.DOTALL)[0].strip()
                purport = re.findall("### Purport:(.*)", content, re.DOTALL)[0].strip()
            else:
                translation = re.findall("### Translation:", content, re.DOTALL)[0].strip()
                purport = ""
            return translation, purport
        except IndexError as i:
            logger.error(f"Error parsing file: {path}")
def process_md_adv(path,headings:list[str])->dict:
    """
    Reads a Markdown (.md) file and returns the required headers
    :param path: path to the Markdown file
    :param headings: list of headings to extract
    :return: a dictionary of the extracted headings
    """
    content = read_file(path)

    resp = dict((zip(headings, [""] * len(headings))))
    resp['Reference'] = ":".join(path.split('/')[-2:]).replace('.md', '')
    if not path.endswith('.md'):
        logger.warning('File extension must be .md', path)
        return resp
    for i in range(len(headings)):
        try:
            key = headings[i]
            pattern = rf"# {key}(.*?)(?=#|$)"
            match = re.search(pattern, content, re.DOTALL)
            match_text = match.group(1) if match else ""
            resp[key] = match_text.replace(':\n\n', ' ').strip()
        except Exception as e:
            logger.error(f"Error parsing file: {path}")
    if not any(resp.values()):
        logger.warning(f"No valid headings found in {path}")
    else:
        logger.info(f"Successfully parsed headings from {path}")
    return resp
