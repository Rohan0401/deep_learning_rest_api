import os


def get_env_var_settings(env_var_name, default_value):
    """
    Returns the environment variables if not present the returns default values
    :param env_var_name: environment variables
    :param default_value: default value to be returned if a variable doesn't exists
    :return: environment variable name
    """

    try:
        env_var_value = os.environ[env_var_name]

    except EnvironmentError:
        env_var_value = default_value

    return env_var_value
