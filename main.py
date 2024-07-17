import logging
from datetime import date

from database.filler import launch_filler
from database.queries import LearningQuery
from database.repositiories.book_repository import BookRepository
from sys import argv


logger = logging.getLogger(__name__)


file_handler = logging.FileHandler(fr'logs\{date.today()}-logs.txt', encoding='utf-8')
file_handler.setLevel(level=logging.DEBUG)

std_handler = logging.StreamHandler()
std_handler.setLevel(level=logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    handlers=[file_handler, std_handler])



def main():
    for func_name, query in LearningQuery.__dict__.items():
        if func_name.startswith('query'):
            print(query())





if __name__ == "__main__":
    path, *args = argv
    if "filler" in args:
        launch_filler()
    else:
        main()
