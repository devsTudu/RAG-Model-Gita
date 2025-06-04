from utils.file_handler import read_file
from utils.logger import get_logger
import re

logger = get_logger(__name__)


def process_md(path: str) -> tuple[str, str] | None:
    """
    Reads a Markdown (.md) file and returns the translation and purport.
    :param path: path to the Markdown file
    :return: a tuple of the translation and purport
    """
    if not path.endswith('.md'):
        logger.warning(' File extension must be .md %s ',path)
    else:
        content = read_file(path)

        try:
            if  "Translation" not in content:
                logger.warning("Translation section not found : %s ",path)
                return "", content
            elif "Purport" in content:
                translation = re.findall("### Translation:(.*?)### Purport:", content, re.DOTALL)[0].strip()
                purport = re.findall("### Purport:(.*)", content, re.DOTALL)[0].strip()
            else:
                translation = re.findall("### Translation:", content, re.DOTALL)[0].strip()
                purport = ""
            return translation, purport
        except IndexError:
            logger.error("Error parsing file: %s ",path)

def process_md_adv(path,headings:list[str])->dict:
    """
    Reads a Markdown (.md) file and returns the required headers
    :param path: path to the Markdown file
    :param headings: list of headings to extract
    :return: a dictionary of the extracted headings
    """
    content = read_file(path)

    resp = dict((zip(headings, [""] * len(headings))))
    if path.endswith('.md'):
        for key in headings:
            try:
                pattern = rf"# {key}(.*?)(?=#|$)"
                match = re.search(pattern, content, re.DOTALL)
                match_text = match.group(1) if match else ""
                resp[key] = match_text.replace(':\n\n', ' ').strip()
            except AttributeError:
                logger.error("Error parsing file: %s", path)
        if not any(resp.values()):
            logger.warning("No valid headings found in %s loading them as content",path)
            resp['content'] = content
        else:
            logger.log(0,"Successfully parsed headings from %s",path)
            
    else:
        logger.warning('File extension must be .md %s ', path)
        
    resp['Reference'] = ":".join(path.split('\\')[-2:]).replace('.md', '')
    return resp
