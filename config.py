import os

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    BASEPATH = os.path.dirname(__file__)
    IMAGE_UPLOAD_LOCATION = os.path.join(BASEPATH, 'data/input_image', 'input.jpg')
    MODEL_NAME = 'Inception_Resnet'
    NO_OF_SIMILAR_IMAGES = 3
    DATASET = 'example_dataset'
    DATASET_IMAGES_PATH = os.path.join(BASEPATH, 'data/dataset', DATASET)
