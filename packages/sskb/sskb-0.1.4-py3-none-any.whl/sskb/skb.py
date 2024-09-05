import os
import gdown
from pathlib import Path
from typing import Sequence
from .data_model import Statement, Entity

BASE_PATH = ".sskb_data"
BASE_URL = "http://personalpages.manchester.ac.uk/staff/danilo.carvalho/sskb/"


class KnowledgeBase(Sequence[Statement]):
    def __init__(self, path: str, url: str, **kwargs):
        self.data_path: str = os.path.normpath(os.path.join(str(Path.home()), BASE_PATH, path))
        if (not os.path.exists(self.data_path) and url):
            os.makedirs(os.path.join(*os.path.split(self.data_path)[:-1]), exist_ok=True)
            gdown.download(url, self.data_path)
        self.id = ""
        self.entities: list[Entity] = list()

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    @staticmethod
    def from_resource(locator: str):
        raise NotImplementedError

    @staticmethod
    def download_resource(path: str, url: str):
        """
        Downloads a resource from a specified URL to a specified path

        This method is used to download original or preprocessed data that backs the KnowledgeBase instances.

        Args:
            path (str): The subpath to the resource within the base path.
            url (str): The URL from which to download the resource.

        Returns:
            str: The normalized path where the resource has been downloaded.
        """
        data_path: str = os.path.normpath(os.path.join(str(Path.home()), BASE_PATH, path))
        if (not os.path.exists(data_path)):
            os.makedirs(os.path.join(*os.path.split(data_path)[:-1]), exist_ok=True)
            gdown.download(url, data_path)

        return data_path



