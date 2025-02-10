from data.dataset_loader import DataLoader

def main():
    dataset = 'retailrocket/ecommerce-dataset'
    download_path = '../data'
    file_name = 'events.csv' 

    loader = DataLoader(dataset, download_path)
    loader.download_data()
    data = loader.load_data(file_name)
    print(data.head())  

if __name__ == "__main__":
    main()