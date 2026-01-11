import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path: str):
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path:str, content:object, replace:bool=True)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,'w') as output_file:
            yaml.dump(content,output_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e