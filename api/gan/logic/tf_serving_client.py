from __future__ import print_function

import os
import operator
import logging
import settings
import utils
import tensorflow as tf

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

log = logging.getLogger (__name__)


def __get_tf_server_conncetion_params__():
    """
    Returns connection parameters to TensorFlow server
    :return: Tuple of TF server name and server port
    """
    server_name = utils.get_env_var_settings ('TF_SERVER_NAME', settings.DEFAULT_TF_SERVER_NAME)
    server_port = utils.get_env_var_settings ('TF_SERVER_PORT', settings.DEFAULT_TF_SERVER_PORT)

    return server_name, server_port


def __create_prediction_request__(image):
    """
    Create prediction request to TensorFlow server for GAN model

    :param image: Byte array of image for prediction
    :return: Predict Request object
    """

    # Create predict request
    request = predict_pb2.PredictRequest ()

    # Call GAN model to make prediction on image
    request.model_spec.name = settings.GAN_MODEL_NAME
    request.model_spec.signature_name = settings.GAN_MODEL_SIGNATURE_NAME
    request.inputs[settings.GAN_MODEL_INPUT_KEY].CopyFrom (
        tf.make_tensor_proto (image, shape=[1])
    )

    return request


def __open_tf_server_channel__(server_name, server_port):
    """
    Open channel to TensorFlow server for request

    :param server_name: String, server name (localhost, IP address)
    :param server_port: String, server port
    :return: channel stub
    """

    channel = implementations.insecure_channel (
        server_name,
        int (server_port))

    stub = prediction_service_pb2.beta_create_PredictionService_stub (channel)

    return stub


def __make_prediction_and_prepare_results__(stub, request):
    """
    Sends Predict request over a channel stub to TensorFlow server
    :param stub: Channel Stub
    :param request: Predict Request object
    :return: List of tuples, 3 most probable digits with their probabilities
    """
    result = stub.Predict (request, 60.0)  # Set 60 sec timeout
    probs = result.outputs['scores'].float_val
    value_dict = {idx: prob for idx, prob in enumerate (probs)}
    sorted_values = sorted (
        value_dict.items (),
        key=operator.itemgetter (1),
        reverse=True
    )

    return sorted_values[0:3]


def make_prediction(image):
    """
    Predict the house number using the iamge from GAN model
    :param image: Byte array of image
    :return:
    """

    # get tensorflow server connection parameters
    server_name, server_port = __get_tf_server_conncetion_params__ ()
    log.info ('Connecting to TensorFLow server %s:%s', server_name, server_port)

    # Open channel to tensorflow server
    stub = __open_tf_server_channel__ (server_name, server_port)

    # Create predict request
    request = __create_prediction_request__ (image)

    # make prediction
    return __make_prediction_and_prepare_results__ (stub, request)
