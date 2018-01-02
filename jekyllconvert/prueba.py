from utils import nb_repo
import os





if __name__ == '__main__':
    here = os.path.dirname(__file__)
    repository = nb_repo(here)
    notebooks = repository.check_log()
    print(notebooks)