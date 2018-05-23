import logging
import traceback

from flask_restplus import Api
import settings


log = logging.getLogger(__name__)

# create Flask-RestPlus API

api = Api(version='1.0',
          title='TensorFlow serving REST Api',
          description='RESTful API wrapper for TensorFlow Serving client')

# Default error handler

@api.errorhandler
def default_error_handler(error):
    """
    Default error handler for unexpected errors

    :param error: Contains specific error information
    :return: Tuple or JSON object with the error information with 500 status code
    """

    message = 'Unexpected error occurred: {}'.format(error.specific)
    log.exception(message)

    if not settings.DEFAULT_FLASK_DEBUG:
        return {'message' : message}, 500
