from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging
from Network_Security.Entity.config_entity import DataIngestionConfig
from Network_Security.Entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
   try:
      trainingpipelinecofig=TrainingPipelineConfig()
      dataingestionconfig = DataIngestionConfig(trainingpipelinecofig)
      dataingestion = DataIngestion(dataingestionconfig)
      logging.info("Initiate the data ingestion")
      dataingestionartifact=dataingestion.initiate_data_ingestion
      print(dataingestionartifact)
      
   except Exception as e:
      raise NetworksecurityException(e,sys)