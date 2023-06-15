from src.flora.config import Configuration
from src.flora.components import DataIngestion
from src.flora import logger
import face_recognition
import torch




def main():
    config = Configuration()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(data_ingestion_config)
    # data_ingestion.download_data()
    # data_ingestion.split_data()
    # data_ingestion.crop_images()
    # data_ingestion.webcam_capture(15)
    # data_ingestion.decode_webcam_images()
    data_ingestion.identify_persons1('qa')
if __name__ =='__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)