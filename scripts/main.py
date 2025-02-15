import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_load import DataLoad
from src.data_processing import DataProcessing
# Main function
def main():
    data_load = DataLoad()
    raw_data = data_load.load_data()

    data_processing = DataProcessing(raw_data)
    data_processing.process_data()

    events = data_processing.preprocess_events()
    category_tree = data_processing.preprocess_category_tree()
    item_properties = data_processing.preprocess_item_properties()

    print(events.head())
    print(category_tree.head())
    print(item_properties.head())


if __name__ == "__main__":
    main()
