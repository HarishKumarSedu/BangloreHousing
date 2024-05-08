import os 
import pandas as pd 
from src.housing.constants import SCHEMA_FILE_PATH, CONFIG_FILE_PATH
from src.housing.utils.common import read_yaml 
from src.housing import log
import json

class DataValidation:
    
    def __init__(self):
        self.schema = read_yaml(SCHEMA_FILE_PATH)
        self.data_ingestion = read_yaml(CONFIG_FILE_PATH).data_ingestion
        self.data_validation = read_yaml(CONFIG_FILE_PATH).data_validation
        # Validate the data columns in the dataset 
        self.data_columns_validation()
        
    def data_columns_validation(self):
        
        dataset = pd.read_csv(self.data_ingestion.local_data_file)
        shcema_data = {}
        shcema_data.update(self.schema.COLUMNS)
        shcema_data.update(self.schema.TARGET)
        
        if not os.path.exists(self.data_validation.root_dir):
            os.makedirs(self.data_validation.root_dir)
        
        columnsValidation_status = True 
        
        for index,column in enumerate(dataset.columns.to_list()):
            # match the column and column type in the dataset 
            if  list(shcema_data.keys())[index] != column and list(shcema_data.values())[index] != dataset[column].dtype:
                log.error(f'Column {column} in the dataset not matching ... Data Columns Validation Failed')
                columnsValidation_status = False
            else:
                log.info(f'Data Column - {column} - Validation Passed Successfully')
                columnsValidation_status = True
                
        with open(os.path.join(self.data_validation.root_dir, self.data_validation.status_file),'w') as file:
            json.dump({"columnValidation":columnsValidation_status},file, )
                