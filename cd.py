__author__ = 'NamelessOne'
import os


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.__newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.__savedPath = os.getcwd()
        os.chdir(self.__newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.__savedPath)