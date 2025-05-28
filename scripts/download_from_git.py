from warnings import warn
from os.path import join
from utils.githubDownloader import Downloader
from utils.file_handler import get_project_root

url = "https://github.com/dbachko/bhagavad-gita-as-it-is"
def main():
    repo = Downloader(url, 'main')
    try:
        repo.download(join(get_project_root(), 'data\\raw'),'en',True)
        print(f"Successfully Downloaded the data from {url}")
    except Exception as e:
        print(f"Unable to get raw data from Git {url}")
        warn(e)