import logging.config
import os
import settings
import utils

from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from api.restplus import api
from api.gan.endpoints.client import ns as gan_client_namespace
# Create Flask application
app = Flask (__name__)

# Load logging configuration and create log object


file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'logging.conf'),
                          disable_existing_loggers=False)
log = logging.getLogger (__name__)


def __get_flask_server_params__():
    """
    Returns connection parameters for the Flask application

    :return: Tuple of server name, server port and debug setting
    """

    server_name = utils.get_env_var_settings ('FLASK_SERVER_NAME', settings.DEFAULT_FLASK_SERVER_NAME)
    server_port = utils.get_env_var_settings ('FLASK_SERVER_PORT', settings.DEFAULT_FLASK_SERVER_PORT)

    flask_debug = utils.get_env_var_settings ('FLASK_DEBUG', settings.DEFAULT_FLASK_DEBUG)
    flask_debug = True if flask_debug == '1' else False

    return server_name, server_port, flask_debug


def configure_app(flask_app, server_name, server_port):
    """
    Configure Flask app

    :param flask_app: Instance of Flask App
    :param server_name: Name of Server
    :param server_port: Port of the Server

    :return:
    """

    flask_app.config['SERVER_NAME'] = server_name + ':' + server_port
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app, server_name, server_port):
    """
    Initialize Flask application with Flask-RestPlus

    :param flask_app: Flask instance
    :param server_name: Server name
    :param server_port: Server Port

    :return:
    """
    blueprint = Blueprint ('tf_api', __name__, url_prefix='/tf_api')

    configure_app (flask_app, server_name, server_port)
    api.init_app (blueprint)
    api.add_namespace(gan_client_namespace)

    flask_app.register_blueprint (blueprint)


def main():
    server_name, server_port, flask_debug = __get_flask_server_params__ ()
    initialize_app (app, server_name, server_port)

    log.info (
        '>>>>>>>> Starting TF Serving client at http://{}/>>>>>'.format (app.config['SERVER_NAME'])

    )
    app.run (debug=flask_debug, host=server_name)


if __name__ == '__main__':
    main ()
