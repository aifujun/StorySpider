import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
LOG_FILE = os.path.join(BASE_DIR, 'log', 'spider.log')


if __name__ == '__main__':
    print(LOG_FILE)
