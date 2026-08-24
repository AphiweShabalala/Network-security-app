from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.data_validation import DataValidation
from Network_Security.Logging.logger import logging

from Network_Security.Entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from Network_Security.Entity.config_entity import TrainingPipelineConfig

import sys

from Network_Security.components.model_trainer import ModelTrainer


if __name__ == '__main__':

    try:

        # =========================================================
        # Training Pipeline Configuration
        # =========================================================

        trainingpipelinecofig = TrainingPipelineConfig()

        # =========================================================
        # Data Ingestion
        # =========================================================

        dataingestionconfig = DataIngestionConfig(
            trainingpipelinecofig
        )

        dataingestion = DataIngestion(
            dataingestionconfig
        )

        logging.info("Initiate the data ingestion")

        dataingestionartifact = (
            dataingestion.initiate_data_ingestion()
        )

        logging.info("Data ingestion completed")

        print(dataingestionartifact)

        # =========================================================
        # Data Validation
        # =========================================================

        data_validation_config = DataValidationConfig(
            trainingpipelinecofig
        )

        data_validation = DataValidation(
            dataingestionartifact,
            data_validation_config
        )

        logging.info("Initiate the data validation")

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        logging.info("Data validation completed")

        print(data_validation_artifact)

        # =========================================================
        # Data Transformation
        # =========================================================

        data_transformation_config = DataTransformationConfig(
            trainingpipelinecofig
        )

        logging.info("Data transformation started")

        data_transformation = DataTransformation(
            data_validation_artifact,
            data_transformation_config
        )

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        logging.info("Data transformation completed")

        print(data_transformation_artifact)

        #=====================================================
        # Model training
        #=====================================================
        logging.info("Model Training Started")
        model_trainer_config=ModelTrainerConfig(trainingpipelinecofig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artfact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")

    except Exception as e:

        raise NetworksecurityException(e, sys)