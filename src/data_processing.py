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
        # Apres avoir fais une Analyse dans jupyter notebook, on a remarqué que la colonne transactionid contient des valeurs manquantes
        # On pas les remplacer car ils correspondent à des évènements qui ne sont pas des transactions
        self.save_processed_data(events, "events")
        return events

    def preprocess_item_properties(self):
        # On va concaténer les deux fichiers item_properties_1 et item_properties_2
        item_prop_1 = pd.read_csv(self.raw_data["item_prop_1"])
        item_prop_2 = pd.read_csv(self.raw_data["item_prop_2"])
        item_properties = pd.concat([item_prop_1, item_prop_2], ignore_index=True)
        # suppresion des doublons
        item_properties.drop_duplicates(inplace=True)
        # conversion de la colonne timestamp en datetime
        item_properties["timestamp"] = pd.to_datetime(item_properties["timestamp"], errors='coerce')
        self.save_processed_data(item_properties, "item_properties")
        return item_properties

    def preprocess_category_tree(self):
        category = pd.read_csv(self.raw_data["category_tree"])
        # suppresion des doublons
        category.drop_duplicates(inplace=True)
        # Apres avoir fais une Analyse dans jupyter notebook, on a remarqué que la colonne parent_category_id contient des valeurs manquantes
        # On va pas les remplacer car ils correspondent à des catégories racines
        category_without_parent = category[category['parentid'].isnull()]
        category_without_parent["categoryid"].count()
        category_level1 = category_without_parent
        category_level2 = category[category['parentid'].isin(category_level1['categoryid'])]
        category_level3 = category[category['parentid'].isin(category_level2['categoryid'])]
        category_level4 = category[category['parentid'].isin(category_level3['categoryid'])]
        category_level5 = category[category['parentid'].isin(category_level4['categoryid'])]
        category_level6 = category[category['parentid'].isin(category_level5['categoryid'])]
        # On va ajouter une colonne level qui indique le niveau de la catégorie
        category_level1.loc['level_tree'] = 1
        category_level2.loc['level_tree'] = 2
        category_level3.loc['level_tree'] = 3
        category_level4.loc['level_tree'] = 4
        category_level5.loc['level_tree'] = 5
        category_level6.loc['level_tree'] = 6

        category_tree_level = pd.concat([category_level1, category_level2, category_level3, category_level4, category_level5, category_level6])
        self.save_processed_data(category_tree_level, "category_tree")
        return category_tree_level