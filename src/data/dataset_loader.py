import os
import kaggle
import pandas as pd

class DataLoader:
    def __init__(self, dataset, download_path):
        self.dataset = dataset
        self.download_path = download_path

    def download_data(self):
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        try:
            kaggle.api.dataset_download_files(self.dataset, path=self.download_path, unzip=True)
            print(f"Dataset downloaded to {self.download_path}")
        except Exception as e:
            print(f"Failed to download dataset: {e}")

    def load_data(self, file_name):
        file_path = os.path.join(self.download_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_name} not found in {self.download_path}")
        data = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
        return data

