from AwstextSummaryJassi07.config.configuration import ConfigurationManager
from AwstextSummaryJassi07.conponents.model_trainer import ModelTrainer
from AwstextSummaryJassi07.logging import logger


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()