from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import sys
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        trainingPipelineConfig = TrainingPipelineConfig()
        dataingestionConfig = DataIngestionConfig(training_pipeline_config=trainingPipelineConfig)
        dataIngestion = DataIngestion(data_ingestion_config=dataingestionConfig)
        logging.info('Start executor')
        data_ingestion_artifact=dataIngestion.initiate_data_ingestion()
        print('Data Ingestion completed successfully')
        print(f'Starting Data Validation with artifact {data_ingestion_artifact}')
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingPipelineConfig)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        print('Initiating Data Validation')
        data_validation.initiate_data_validation() 
        print('Data Validation Completed successfully')
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e