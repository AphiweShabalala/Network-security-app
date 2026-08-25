import os
import sys

from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging

from Network_Security.cloud.s3_syncer import S3Sync
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_trainer import ModelTrainer

from Network_Security.Entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from Network_Security.Entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from Network_Security.constants.training_pipeline import TRAINING_BUCKET_NAME


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync= S3Sync()
         
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data Ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Initiate the data validation")
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transform_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transform_config)

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataValidationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config:ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            model_trainer = ModelTrainer(
                data_transformation_artfact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buckek_url=aws_bucket_url)
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url= f"s3://{TRAINING_BUCKET_NAME}/final_model{self.training_pipeline_config}"
            self.s3_sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
        
    def run_pipeline(self):
        try:
          data_ingestion_artifact= self.start_data_ingestion()
          data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
          model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
          
          self.sync_artifact_dir_to_s3()
          self.sync_saved_model_dir_to_s3()
          return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)