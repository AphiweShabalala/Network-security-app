from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.components.data_validation import DataValidation
from Network_Security.Logging.logger import logging
from Network_Security.Entity.config_entity import DataIngestionConfig,DataValidationConfig
from Network_Security.Entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
   try:
      trainingpipelinecofig=TrainingPipelineConfig()
      dataingestionconfig = DataIngestionConfig(trainingpipelinecofig)
      dataingestion = DataIngestion(dataingestionconfig)
      logging.info("Initiate the data ingestion")
      dataingestionartifact=dataingestion.initiate_data_ingestion()
      logging.info("Data initiation completed")
      print(dataingestionartifact)
      data_validation_config=DataValidationConfig(trainingpipelinecofig)
      data_validation = DataValidation(dataingestionartifact,data_validation_config)
      logging.info("Initiate the data validation")
      data_validation_artifact = data_validation.initiate_data_validation()
      logging.info("data validation completed")
      print(data_validation_artifact)
      
   except Exception as e:
      raise NetworksecurityException(e,sys)