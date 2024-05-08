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
