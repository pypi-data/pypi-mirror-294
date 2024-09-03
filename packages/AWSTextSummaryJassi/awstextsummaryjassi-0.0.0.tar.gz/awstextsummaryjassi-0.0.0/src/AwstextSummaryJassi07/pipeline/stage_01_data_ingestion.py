from AwstextSummaryJassi07.config.configuration import ConfigurationManager
from AwstextSummaryJassi07.conponents.data_ingestion import DataIngestion
from AwstextSummaryJassi07.logging import logger


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()