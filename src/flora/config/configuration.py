from src.flora.utils import read_yaml,create_directories
from src.flora.constants import CONFIG_FILE_PATH
from src.flora.entity import DataIngestionConfig
from box import ConfigBox


class Configuration:
    def __init__(self,config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        create_directories([config.crop_images_dir])
        create_directories([config.images_dir])
        create_directories([config.webcam_img_dir])
        create_directories([config.decode_img_dir])
        create_directories([config.unknown_faces_dir])

        data_ingestion = DataIngestionConfig(root_dir=config.root_dir,
                            crop_images_dir=config.crop_images_dir,
                            images_dir=config.images_dir,
                            webcam_img_dir=config.webcam_img_dir,
                            decode_img_dir=config.decode_img_dir,
                            unknown_faces_dir=config.unknown_faces_dir)
        

        
        return data_ingestion



        


ob = Configuration()
ob.get_data_ingestion_config()


