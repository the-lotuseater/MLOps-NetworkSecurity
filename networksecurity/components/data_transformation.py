import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_np_array, save_object

class DataTransformation:
    def __init__(self,data_valiation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_valiation_artifact
            self.data_transformation_config = data_transformation_config


        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    @staticmethod
    def read_data(file_path:str):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
              
    def get_data_transformer_object(self)->Pipeline:
        logging.info('Enter')
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info('Initialized knn imputer')
            proccessor = Pipeline([('imputer',imputer)])

            return proccessor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        logging.info('Exit')   

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        logging.info('Enter')
        try:
            train_df = DataTransformation.read_data(file_path=self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(file_path=self.data_validation_artifact.valid_test_file_path)
            #training and testing df
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            #preprocessing
            pre_proccessor = self.get_data_transformer_object()
            pre_processor_obj = pre_proccessor.fit(input_feature_train_df)
            processed_input_feature_train_df = pre_processor_obj.transform(input_feature_train_df)
            processed_input_feature_test_df = pre_processor_obj.transform(input_feature_test_df)

            train_arr = np.c_[processed_input_feature_train_df, np.array(target_feature_train_df)]
            test_arr = np.c_[processed_input_feature_test_df, np.array(target_feature_test_df)]
            logging.info('Saving processed numpy arrays')
            
            save_np_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_np_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, pre_processor_obj)

            save_object('final_model/preprocessor.pkl', pre_processor_obj)
            logging.info('Preparing data transformation artifact')
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e



