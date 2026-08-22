from Network_Security.Entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Network_Security.Entity.config_entity import DataValidationConfig
from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging
from Network_Security.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from Network_Security.constants.training_pipeline import SCHEMA_FILE_PATH
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e :
            raise NetworksecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworksecurityException(e,sys)


    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
      try:
        schema_columns = [
            list(column.keys())[0]
            for column in self._schema_config["columns"]
        ]

        dataframe_columns = dataframe.columns.tolist()

        logging.info(
            f"Required number of columns: {len(schema_columns)}"
        )

        logging.info(
            f"Data frame has columns: {len(dataframe_columns)}"
        )

        missing_columns = set(schema_columns) - set(dataframe_columns)
        extra_columns = set(dataframe_columns) - set(schema_columns)

        if missing_columns:
            logging.error(
                f"Missing columns: {missing_columns}"
            )

        if extra_columns:
            logging.error(
                f"Extra columns: {extra_columns}"
            )

        return len(missing_columns) == 0 and len(extra_columns) == 0

      except Exception as e:
        raise NetworksecurityException(e, sys)

    
    def detect_dataset_drifts(self, base_df, current_df, threshold=0.05) -> bool:
      try:
        status = True
        report = {}

        for column in base_df.columns:
            d1 = base_df[column]
            d2 = current_df[column]

            is_sample_dist = ks_2samp(d1, d2)

            if threshold <= is_sample_dist.pvalue:
                is_found = False
            else:
                is_found = True
                status = False

            report.update({
                column: {
                    "p_value": float(is_sample_dist.pvalue),
                    "drift_status": is_found
                }
            })

        drift_report_file_path = self.data_validation_config.drift_report_file_path

        # Creating directory
        dir_path = os.path.dirname(drift_report_file_path)
        os.makedirs(dir_path, exist_ok=True)

        write_yaml_file(
            file_path=drift_report_file_path,
            content=report
        )

        return status

      except Exception as e:
        raise NetworksecurityException(e, sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            ## validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all column.\n"
                raise ValueError(error_message)
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)

            if not status:
                     error_message=f"Test dataframe does not contain all column.\n" 
                     raise ValueError(error_message)

            ##Checking datadrift
            status=self.detect_dataset_drifts(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                 self.data_validation_config.valid_train_file_path, index=False, header=True
            )   

            
            test_dataframe.to_csv(
                 self.data_validation_config.valid_test_file_path, index=False, header=True
            )   

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path, ## self.data...->  valid_train_file_path=self.data_validation_config.valid_train_file_path
                valid_test_file_path= self.data_validation_config.valid_test_file_path, ##self.dat...-> valid_test_file_path=self.data_validation_config.valid_test_file_path
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path= self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
                        
        except Exception as e:
            raise NetworksecurityException(e,sys)

    