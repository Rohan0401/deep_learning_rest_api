# Flask settings
DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
DEFAULT_FLASK_SERVER_PORT = '5001'
DEFAULT_FLASK_DEBUG = True  # Remove debug mode in production mode

# Flask-RestFulPlus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# GAN Client settings

DEFAULT_TF_SERVER_NAME = '172.17.0.2'
DEFAULT_TF_SERVER_PORT = 9000
GAN_MODEL_NAME = 'gan'
GAN_MODEL_SIGNATURE_NAME = 'predict_images'
GAN_MODEL_INPUT_KEY = 'images'
