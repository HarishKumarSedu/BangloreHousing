
import os 
import json
import pandas as pd
from src.housing.constants import CONFIG_FILE_PATH, SCHEMA_FILE_PATH

from src.housing.utils.common import read_yaml
from src.housing import log
import re 

class DataTransforamation:

    def __init__(self) -> None:
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.data_ingestion = self.config.data_ingestion
        self.data_validation = self.config.data_validation
        #import the schema
        self.schema = read_yaml(SCHEMA_FILE_PATH)
        #get the data validation status file 
        validation_status_file = os.path.join(self.data_validation.root_dir,self.data_validation.status_file)
        #check for the dataset 
        if os.path.exists(self.data_ingestion.local_data_file):
            self.dataset = pd.read_csv(self.data_ingestion.local_data_file)
        else:
            log.error(f'Data set dose not present in artifacts ...!')
        #Load the json validation status file data 
        if os.path.exists(validation_status_file) :
            with open(validation_status_file, 'r') as file :
                self.validation_status_data = json.load(file)
        else:
            log.error(f'Validation Status file {validation_status_file} dose not exists in artifacts')
        #Data imputation 
        self.data_imputation()
        #Data Feature Engineering 
        self.data_feature_engineering()
    def data_imputation(self):
        if self.validation_status_data.get('columnValidation') :
            #drop the na values since it is the big dataset set
            # it is ok! to sacrifies few NA data points 
            if max(self.dataset.isna().sum().to_dict().values()) > 0 :
                self.dataset.dropna(inplace=True)
                log.warn(f'droped NAN value rows from data set \n{self.dataset.isna().sum()}')
        else:
            log.error(f'Data columns not validated ....! data imputation failed')
            
    def data_feature_engineering(self):
        newfeatures = self.schema.NEWFEATURES
        if self.validation_status_data.get('columnValidation') :
            # extract the bedrooms 
            def extract_bedrooms(x):
                BHK = 0
                if BHK := re.findall('[0-9]+',x)[0]:
                    BHK = int(BHK,16)
                return  BHK
            self.dataset[newfeatures.BHK] =self.dataset['size'].apply(extract_bedrooms)
            self.dataset.drop(['size'], inplace=True, axis=1)
            log.info(f'From the size column New feature "BHK" added in to the data set   ')
            ###
            #@ Add new feature price per squre feet 
            # with open('test.json','w') as file:
            #     json.dump(self.dataset['total_sqft'].unique().tolist(),file)
            
        else:
            log.error(f'Data columns not validated ....! data feature engineering failed')