
import os 
import json
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from src.housing.constants import CONFIG_FILE_PATH, SCHEMA_FILE_PATH
from src.housing.utils.common import read_yaml
from src.housing import log
import re 

class DataTransforamation:

    def __init__(self) -> None:
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.data_ingestion = self.config.data_ingestion
        self.data_validation = self.config.data_validation
        self.data_transformation = self.config.data_transformation
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
        # remove the outliers from the price_per_sqft 
        self.data_outlier_removing()
        # split train and test data 
        self.split_data()
    #########
    #####
    #########
    def data_imputation(self):
        if self.validation_status_data.get('columnValidation') :
            #drop the na values since it is the big dataset set
            # it is ok! to sacrifies few NA data points 
            if max(self.dataset.isna().sum().to_dict().values()) > 0 :
                self.dataset.dropna(inplace=True)
                log.warn(f'droped NAN value rows from data set \n{self.dataset.isna().sum()}')
        else:
            log.error(f'Data columns not validated ....! data imputation failed')
    ###########
    ######
    ##########
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
            # self.dataset.drop(['size'], inplace=True, axis=1)
            log.info(f'From the size column New feature "BHK" added in to the data set   ')
            ###
            #@ Add new feature price per squre feet 
            def extract_sqft(sqft):
                square_feet = 0
                if '-' in sqft:
                    sqft = sqft.split('-')
                    if length:= len(sqft) == 2:
                        sqft1= re.findall(r"[-+]?(?:\d*\.*\d+)", sqft[0])[0]
                        sqft2= re.findall(r"[-+]?(?:\d*\.*\d+)", sqft[1])[0]
                        square_feet = (float(sqft1) + float(sqft2))/2

                elif 'Sq. Meter' in sqft:
                    square_feet = float(re.findall(r"[-+]?(?:\d*\.*\d+)", sqft)[0])*10.7639
                elif 'Sq. Yards' in sqft:
                    square_feet = float(re.findall(r"[-+]?(?:\d*\.*\d+)", sqft)[0])*9
                else:
                    square_feet = float(re.findall(r"[-+]?(?:\d*\.*\d+)", sqft)[0])
                return square_feet
            ###
            ## @ extracting the total squre feet data
            ###
            self.dataset['total_sqft']=self.dataset['total_sqft'].apply(extract_sqft)
            log.info(f'Total Square Feet cleaned from total_sqft ...!')
            ###
            ## @ Add New Feature 
            ## @ PPS - price_per_sqft
            ###
            self.dataset[newfeatures.PPS]=self.dataset['price']*1000000/self.dataset['total_sqft']           
            ###
            ## @ Add New Feature 
            ## @ PPS - price_per_sqft
            ###
            log.info(f'Price per Square feet feature added intot the dataset "price_per_sqft" ...!')
        else:
            log.error(f'Data columns not validated ....! data feature engineering failed')
    ###
    ## @ Add New Feature 
    ## @ PPS - price_per_sqft
    ###
    def data_outlier_removing(self):
        def remove_pps_outliers(df):
            df_out=pd.DataFrame()
            for key,subdf in df.groupby('location'):
                m=np.mean(subdf.price_per_sqft)
                st=np.std(subdf.price_per_sqft)
                reduced_df=subdf[(subdf.price_per_sqft>(m-st))& (subdf.price_per_sqft<(m+st))]
                df_out=pd.concat([df_out,reduced_df],ignore_index=True)
            return df_out
        self.dataset=remove_pps_outliers(self.dataset)
        log.info(f'outliers removed from "price_per_sqft" ...!')
        ######
        ## @ remove the outlier from the bhk 
        ######
        def remove_bhk_outliers(df):
            exclude_indices=np.array([])
            for location, location_df in df.groupby('location'):
                bhk_sats={}
                for BHK,BHK_df in location_df.groupby('bhk'):
                    bhk_sats[BHK]={
                        'mean':np.mean(BHK_df.price_per_sqft),
                        'std':np.std(BHK_df.price_per_sqft),
                        'count':BHK_df.shape[0]
                    }
                for BHK,BHK_df in location_df.groupby('bhk'):
                    stats=bhk_sats.get(BHK-1)
                    if stats and stats['count']>5:
                        exclude_indices=np.append(exclude_indices,BHK_df[BHK_df.price_per_sqft<(stats['mean'])].index.values)
            return df.drop(exclude_indices,axis='index')
        #######
        ### @ 
        ######
        self.dataset=remove_bhk_outliers(self.dataset)
        log.info(f'outliers removed from "bhk" ...!')
        #### @ one hot encode the location 
        ####
        ########
        dummies = pd.get_dummies(self.dataset['location'])
        self.dataset=pd.concat([self.dataset,dummies],axis='columns')
        log.info(f'location columns one hot encoded ...!')
        ######
        ## @ Drop columns 
        ##########
        self.dataset=self.dataset.drop(self.schema.DROPCOLUMNS.values(),axis='columns')
        log.info(f'columns {self.schema.DROPCOLUMNS.values()} dropped from dataset ...!')
    ########
    ## @ Split train and test data 
    ########
    def split_data(self):
        if not os.path.exists(self.data_transformation.root_dir):
            os.makedirs(self.data_transformation.root_dir)
        
        if os.path.exists(self.data_ingestion.local_data_file) :
            
            train, test = train_test_split(self.dataset)
            train.to_csv(os.path.join(self.config.data_ingestion.root_dir, self.data_transformation.train_data),index = False)
            test.to_csv(os.path.join(self.config.data_ingestion.root_dir, self.data_transformation.test_data),index = False)
            log.info('Trian and Test Data splited ...!')
        else:
            log.error(f'Data dose not exists {self.data_ingestion.local_data_file}')