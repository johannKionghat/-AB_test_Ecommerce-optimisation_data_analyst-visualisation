
from config import KAGGLE_DATASET, RAW_DATA_PATH
from kaggle.api.kaggle_api_extended import KaggleApi
import os


class DataLoad:
    def __init__(self, datasets=None):
        self.save_raw_data_path = RAW_DATA_PATH
        self.dataset_path = KAGGLE_DATASET
        self.datasets = datasets or {
            "category_tree": "category_tree.csv",
            "events": "events.csv",
            "item_prop_1": "item_properties_part1.csv",
            "item_prop_2": "item_properties_part2.csv",
        }
        self.api = KaggleApi()
        self.api.authenticate()

    def download_data(self):
        self.api.dataset_download_files(self.dataset_path, path=self.save_raw_data_path, unzip=True)
        print("Data downloaded successfully.")

    def load_data(self):
        datasets = {}
        for key, filename in self.datasets.items():
            file_path = os.path.join(self.save_raw_data_path, filename)
            if not os.path.exists(file_path):
                print(f"{filename} not found, downloading data from Kaggle.")
                self.download_data()
            datasets[key] = file_path
        print("Data loaded successfully.")
        return datasets
