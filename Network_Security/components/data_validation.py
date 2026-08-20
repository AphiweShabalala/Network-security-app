from Network_Security.Entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Network_Security.Entity.config_entity import DataValidationConfig
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging
from scipy.stats import ks_2samp
import pandas
import os,sys
from Network_Security.constants.training_pipeline import SCHEMA_FILE_PATH
from Network_Security.utils.main_utils.utils import read_yaml_file
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e :
            raise NetworksecurityException(e,sys)
         