import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processing import DataProcessing

def main():
    data_processing = DataProcessing()
    data_processing.process_data()
    data_processing.preprocess_events()
    data_processing.preprocess_item_properties()
    data_processing.preprocess_category_tree()
    
main() 