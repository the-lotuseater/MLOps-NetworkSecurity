from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp#check 2 samples of data for data drift
import pandas as pd
import sys
import os


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod 
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_columns(self,dataFrame: pd.DataFrame)->bool:
        try:
            n_columns = len(self._schema_config['columns'])
            logging.info(f'Required number of columns: {n_columns}')
            logging.info(f'DataFrame has columns: {len(dataFrame.columns)}')
            if len(dataFrame.columns) == n_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame, threshold=0.5):
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                ks_2samp_result = ks_2samp(d1,d2)
                p_value = ks_2samp_result.pvalue
                if p_value < threshold:
                    is_found = True
                    status = False
                else:
                    is_found = False
                report.update({col:{
                    'p_value':float(p_value),
                    'drift_status':is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ## read data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            ## validate number of columns

            status = self.validate_number_of_columns(train_df)
            if not status:
                error_msg = f'{error_msg} Train DataFrame does not contain all columns.\n'
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_msg = f'{error_msg} Test DataFrame does not contain all columns.\n'
            
            ##lets check data drift
            status = self.detect_data_drift(base_df=train_df,current_df=test_df)
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path,exist_ok=True)
                train_df.to_csv(
                    self.data_validation_config.valid_train_file_path,index=False,header=True
                )
                test_df.to_csv(
                    self.data_validation_config.valid_test_file_path,index=False,header=True
                )

                data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
                logging.info(f'Data Validation artifact created: {data_validation_artifact}')
        except Exception as e:
            raise NetworkSecurityException(e, sys)