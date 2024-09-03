from AwstextSummaryJassi07.config.configuration import ConfigurationManager
from AwstextSummaryJassi07.conponents.model_evaluation import ModelEvaluation
from AwstextSummaryJassi07.logging import logger




class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
        model_evaluation_config.evaluate()