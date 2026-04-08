from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.constants import training_pipeline

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
from networksecurity.cloud.s3_syncer import S3Syncer

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Syncer()
    
    def start_data_ingestion(self):
        try:
            self.dataingestionConfig = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            dataIngestion = DataIngestion(data_ingestion_config=self.dataingestionConfig)
            data_ingestion_artifact=dataIngestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion completed successfully {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting data ingestion: {e}')
            raise NetworkSecurityException(e,sys) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation() 
            logging.info('Data Validation Completed successfully')
            return data_validation_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting data validation: {e}')
            raise NetworkSecurityException(e,sys) from e
    
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
            raise NetworkSecurityException(e,sys) from e
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info('All the components of pipeline completed successfully..starting model training')
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info('Model Training Artifact created')
            return model_trainer_artifact
        except Exception as e:
            logging.error(f'Error occurred while starting model trainer: {e}')
            raise NetworkSecurityException(e,sys) from e
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_saved_model_to_s3()
            return model_trainer_artifact
        except Exception as e:
            logging.error(f'Error occurred while running the training pipeline: {e}')
            raise NetworkSecurityException(e,sys) from e
    
    def sync_artifact_to_s3(self):
        try:
            aws_bucket_url = f's3://{training_pipeline.TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(local_folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logging.error(f'Error occurred while syncing artifact to s3: {e}')
            raise NetworkSecurityException(e,sys) from e
        
    def sync_saved_model_to_s3(self):
        try:
            aws_bucket_url = f's3://{training_pipeline.TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(local_folder=self.training_pipeline_config.final_model_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logging.error(f'Error occurred while syncing artifact to s3: {e}')
            raise NetworkSecurityException(e,sys) from e
    
    