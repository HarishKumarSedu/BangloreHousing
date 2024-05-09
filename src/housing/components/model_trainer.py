
import os 
import json
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from src.housing.constants import CONFIG_FILE_PATH, SCHEMA_FILE_PATH
from src.housing.utils.common import read_yaml
from src.housing import log
from sklearn.linear_model import LinearRegression

class ModelTrainer:

    def __init__(self) -> None:
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.data_ingestion = self.config.data_ingestion
        self.data_validation = self.config.data_validation
        self.data_transformation = self.config.data_transformation