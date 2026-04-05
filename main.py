from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        trainingPipelineConfig = TrainingPipelineConfig()
        dataingestionConfig = DataIngestionConfig(training_pipeline_config=trainingPipelineConfig)
        dataIngestion = DataIngestion(data_ingestion_config=dataingestionConfig)
        logging.info('Start executor')
        data_ingestion_artifact=dataIngestion.initiate_data_ingestion()
        logging.info(f'Data Ingestion completed successfully {data_ingestion_artifact}')
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingPipelineConfig)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        logging.info('Initiating Data Validation')
        data_validation_artifact = data_validation.initiate_data_validation() 
        logging.info('Data Validation Completed successfully')
        logging.info('Initiating Data Transformation')
        dataTransformationConfig = DataTransformationConfig(training_pipeline_config=trainingPipelineConfig)
        data_transformation = DataTransformation(data_valiation_artifact=data_validation_artifact,
                                 data_transformation_config=dataTransformationConfig)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f'Data Transformation completed successfully {data_transformation_artifact}')

        logging.info('All the components of pipeline completed successfully..starting model training')
        ModelTrainerConfig = ModelTrainerConfig(trainingPipelineConfig)
        model_trainer = ModelTrainer(model_trainer_config=ModelTrainerConfig,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info('Model Training Artifact created')

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e