from Network_Security.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_DIR_NAME

import os
import sys

from Network_Security.Exception.exception import NetworksecurityException
from Network_Security.Logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworksecurityException(e,sys)
        