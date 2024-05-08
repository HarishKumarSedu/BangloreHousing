
import os 
from src.housing.constants import  CONFIG_FILE_PATH, KAGGLE_AUTH_PATH
from src.housing.utils.common import read_yaml, get_size
import json 
from src.housing import log

class DataIgestion:
    
    def __init__(self) -> None:
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.kaggle_auth_filepath = KAGGLE_AUTH_PATH
        
        self.download_data()
            
    def download_data(self):
        # create the artifacts root_directory 
        artifacts_dir = self.config.artifacts_root
        if not os.path.exists(artifacts_dir) :
            os.makedirs(artifacts_dir)
        
        with open(self.kaggle_auth_filepath, 'r') as file :
            kaggle_auth = json.load(file)
            
        os.environ['KAGGLE_USERNAME'] = kaggle_auth.get('username')
        os.environ['KAGGLE_KEY'] = kaggle_auth.get('key')
        from kaggle import api 
        api.dataset_download_files(self.config.data_ingestion.source_URL, path=self.config.data_ingestion.root_dir, unzip=True)
        try:
            with open(self.config.data_ingestion.local_data_file, 'r') as file :
                directory, filename = os.path.split(self.config.data_ingestion.local_data_file)
                log.info(f'Data laded successfully with filename {filename} ')
        except:
            log.error(f'Loading data is failed ....!')