from src.housing import log
import os 
import opendatasets as od 

import urllib.request as request 

def download_file():
    od.download(
            dataset_id_or_url = 'https://www.kaggle.com/amitabhajoy/bengaluru-house-price-data',
        )

download_file()