# BangloreHousing

<h3> Create the logger under the project (inside __init__.py ) with rich text </h3>

``` 
import os 
import sys 
import logging
from rich.logging import RichHandler

# # setup the loggins string format 
logging_str = "[%(asctime)s : %(levelname)s : %(module)s : %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir,"running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level="NOTSET", format=logging_str, datefmt="", handlers=[
        RichHandler(),
        logging.FileHandler(log_filepath),
                                                                  ]
)  
log = logging.getLogger(__name__)

```
<h3> Data Pipelines </h3>
<ol>
<li> data Ingestion </li>
<li> data Validation </li>
<li> data Transformation </li>
<li> Model Training </li>
<li> Model Evaluvating </li>
<li> CI </li>
<li> CT </li>
<li> CD </li>
<li> CI-CT-CD </li>
</ol>

1. Data Ingestion 

    - Define Path of the config files under the *** src/housing/constants/__init__.py ***
        ```
        CONFIG_FILE_PATH = Path("config/config.yaml")
        PARAMS_FILE_PATH = Path("params.yaml")
        SCHEMA_FILE_PATH = Path("schema.yaml") 
        ```

    - define the download_data inside the ``` components/data_ingestion/DataIngestion``` 
        - download data from kaggle, for importing the kaggle library  define the kaggle authentication  varaibles ```{"username":"username","key":"key"}``` ``` kaggle/kaggle.json ``` before you import the kaggle library 
        
            ```         
            with open(self.kaggle_auth_filepath, 'r') as file :
            kaggle_auth = json.load(file)
            
            os.environ['KAGGLE_USERNAME'] = kaggle_auth.get('username')
            os.environ['KAGGLE_KEY'] = kaggle_auth.get('key')
            from kaggle import api 
            api.dataset_download_files(self.config.data_ingestion.source_URL, path=self.config.data_ingestion.root_dir, unzip=True)
            ``` 