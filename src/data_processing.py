from src.data_load import DataLoad
from config import PROCESSED_DATA_PATH, RAW_DATA_PATH
import os
import pandas as pd

class DataProcessing:
    def __init__(self, raw_data=None):
        self.raw_data = raw_data or DataLoad().load_data()
        self.processed_data_path = PROCESSED_DATA_PATH
        os.makedirs(self.processed_data_path, exist_ok=True)

    def process_data(self):
        for dataset, file_path in self.raw_data.items():
            processed_file_path = os.path.join(self.processed_data_path, f"p_{dataset}.csv")
            if not os.path.exists(processed_file_path):
                df = pd.read_csv(file_path)
                self.save_processed_data(df, dataset)
                print(f"{dataset} processed successfully.")
            else:
                print(f"{dataset} already processed.")

    def save_processed_data(self, dataframe, dataset):
        output_path = os.path.join(self.processed_data_path, f"p_{dataset}.csv")
        dataframe.to_csv(output_path, index=False)
        print(f"{dataset} data saved successfully.")

    def preprocess_events(self):
        events = pd.read_csv(self.raw_data["events"])
        # suppresion des doublons
        events.drop_duplicates(inplace=True)
        # conversion de la colonne timestamp en datetime
        events["timestamp"] = pd.to_datetime(events["timestamp"], errors='coerce')
        events["date"] = events["timestamp"].dt.date
        events["hour"] = events["timestamp"].dt.hour
        events["second"] = events["timestamp"].dt.second
        self.save_processed_data(events, "events")
        return events

    def preprocess_item_properties(self):
        item_prop_1 = pd.read_csv(self.raw_data["item_prop_1"])
        item_prop_2 = pd.read_csv(self.raw_data["item_prop_2"])
        item_properties = pd.concat([item_prop_1, item_prop_2], ignore_index=True)
        # suppresion des doublons
        item_properties.drop_duplicates(inplace=True)
        self.save_processed_data(item_properties, "item_properties")
        return item_properties

    def preprocess_category_tree(self):
        category_tree = pd.read_csv(self.raw_data["category_tree"])
        # suppresion des doublons
        category_tree.drop_duplicates(inplace=True)
        self.save_processed_data(category_tree, "category_tree")
        return category_tree