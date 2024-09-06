import os

import dvc


class DataLoader:
    def __init__(self):
        self.data_directory = os.path.join(__file__, "data")
        self.repo_path = "https://github.com/osirixgrpc/pyosirix_example_project"

    @property
    def text_file_path(self) -> str:
        return os.path.join(self.data_directory, "viewer_text.txt")

    def __download_text_data__(self):
        """ Load the text data from DVC repository
        """
        with dvc.api.open(self.text_file_path, repo=self.repo_path) as f:
            with open(model_path, 'wb') as model_file:
                model_file.write(f.read())
        print(f"Model '{model_path}' successfully pulled from DVC.")
    def text_data(self) -> str:
        """ Get the content of the text data file.

        Returns:
            str: Content of the text data file.
        """
        if not os.path.exists(text_data_file):

