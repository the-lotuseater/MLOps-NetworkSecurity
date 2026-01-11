from networksecurity.components.data_ingestion import DataIngestion
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
        dataIngestion.initiate_data_ingestion()
        print('Data Ingestion completed successfully')
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e