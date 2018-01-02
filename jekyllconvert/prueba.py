from utils import nb_repo  # Used to get the repository information
import os
from jekyllconvert import jekyll_export




if __name__ == '__main__':
    here = os.path.dirname(__file__)
    repository = nb_repo(here)
    notebooks = repository.check_log()
    for i in notebooks['notebooks']:
        print(i)