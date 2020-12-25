import os


basepath = os.path.dirname(__file__)
file_path = os.path.join(basepath, 'data/input_image', 'input.jpg')

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    IMAGE_UPLOAD_LOCATION = file_path
