from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_ingestion import DataIngestion

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
import sys

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.dataingestionConfig = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            dataIngestion = DataIngestion(data_ingestion_config=self.dataingestionConfig)
            data_ingestion_artifact=dataIngestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion completed successfully {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting data ingestion: {e}')
            raise NetworkSecurityException(e) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation() 
            logging.info('Data Validation Completed successfully')
            return data_validation_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting data validation: {e}')
            raise NetworkSecurityException(e) from e
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_valiation_artifact=data_validation_artifact,
                                 data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f'Data Transformation completed successfully {data_transformation_artifact}')
            return data_transformation_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting data transformation: {e}')
            raise NetworkSecurityException(e) from e
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info('All the components of pipeline completed successfully..starting model training')
            ModelTrainerConfig = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=ModelTrainerConfig,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info('Model Training Artifact created')
            return model_trainer_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting model trainer: {e}')
            raise NetworkSecurityException(e) from e
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            logging.error(f'Error occurred while running the training pipeline: {e}')
            raise NetworkSecurityException(e) from e