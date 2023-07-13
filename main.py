from src.flora.config import Configuration
from src.flora.components import DataIngestion
from src.flora import logger
import face_recognition





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











# from src.flora.config import Configuration
# from src.flora.components import DataIngestion
# from src.flora import logger
# import face_recognition
# from src.flora.components import FaceDetectorCNN 
# import argparse


# # -----parameters added for command line interface (Zeeshan)--------------------
# def main():
#     # Create an ArgumentParser object
#     parser = argparse.ArgumentParser(description='Face Detection and Recognition')

#     # Add command-line arguments
#     parser.add_argument('--video', type=str, default='0', help='Video source (default: 0 for webcam)')
#     parser.add_argument('--tolerance', type=float, default=0.6, help='Tolerance for face recognition (default: 0.6)')


#      # Parse the command-line arguments
#     args = parser.parse_args()

#     # Extract the values
#     video_source = args.video
#     tolerance = args.tolerance

#     # Create an instance of FaceDetectorCNN with the extracted values
#     face_detector = FaceDetectorCNN(video_source=video_source, tolerance=tolerance)

#     # Call the capture_frames method
#     face_detector.capture_frames()



# if __name__ =='__main__':
#     try:
#         main()
#     except Exception as e:
#         logger.exception(e)
#         logger.exception(e)
