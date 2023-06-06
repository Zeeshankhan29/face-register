from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    crop_images_dir : Path
    images_dir : Path
    webcam_img_dir :  Path
    decode_img_dir : Path
    unknown_faces_dir : Path




# @dataclass(frozen=True)
# class DataTransformationConfig:
#     train_dir :Path
#     test_dir :Path
#     root_dir :Path
#     pickle_dir:Path
#     transformed_train_dir : Path
#     transformed_test_dir : Path


# @dataclass(frozen=True)
# class ModelTrainingConfig:
#     transformed_train_dir: Path
#     tranformed_test_dir:Path
#     pickle_dir :str
#     parameter_dir:Path

# @dataclass(frozen=True)
# class ModelPusherConfig:
#     pickle_dir : Path
#     s3_bucket_pickle : 