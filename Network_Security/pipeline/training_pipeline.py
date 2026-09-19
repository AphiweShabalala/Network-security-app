import sys

from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging

from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_trainer import ModelTrainer

from Network_Security.Entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from Network_Security.Entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)


class TrainingPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            logging.info("Start Data Ingestion")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info(
                f"Data ingestion completed and artifact: "
                f"{data_ingestion_artifact}"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)

    def start_data_validation(
        self,
        data_ingestion_artifact: DataIngestionArtifact
    ):

        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )

            logging.info("Initiate the data validation")

            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )

            if not data_validation_artifact.validation_status:
                raise ValueError(
                    "Dataset drift was detected. Review the drift report before training."
                )

            return data_validation_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)

    def start_data_transformation(
        self,
        data_validation_artifact: DataValidationArtifact
    ):

        try:
            data_transform_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transform_config
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)

    def start_model_trainer(
        self,
        data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:

        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artfact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )

            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)

    def run_pipeline(self):

        try:

            # 1. Data Ingestion
            data_ingestion_artifact = (
                self.start_data_ingestion()
            )

            # 2. Data Validation
            data_validation_artifact = (
                self.start_data_validation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            if not data_validation_artifact.validation_status:
                raise ValueError(
                    "Dataset drift was detected. Review the drift report before training."
                )

            # 3. Data Transformation
            data_transformation_artifact = (
                self.start_data_transformation(
                    data_validation_artifact=data_validation_artifact
                )
            )

            # 4. Model Training
            model_trainer_artifact = (
                self.start_model_trainer(
                    data_transformation_artifact=data_transformation_artifact
                )
            )

            logging.info(
                "Training pipeline completed successfully."
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys)
