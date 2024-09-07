
import os

from .utils import read_yaml, set_environment_config, set_logging


class SetEnvironment:
    """
    A class to set up the environment configuration for the project.

    This class reads environment and credentials configuration from YAML files,
    sets up the environment based on the specified environment name, and
    optionally configures logging.

    Attributes:
        credentials (dict): Credentials loaded from the credentials YAML file.
        environment_config (dict): Environment configuration for the specified environment.
        logger (logging.Logger): Logger object if config_logger is True.

    Args:
        root_dir (str): Root directory of the project.
        environment_name (str): Name of the environment to set up. Defaults to "DEV".
        environment_path (str): Path to the environment YAML file, relative to root_dir. Defaults to "conf/local/environment.yml".
        credentials_path (str): Path to the credentials YAML file, relative to root_dir. Defaults to "conf/local/credentials.yml".
        config_logger (bool): Whether to configure logging. Defaults to True.
    """

    def __init__(
        self,
        root_dir,
        environment_name="DEV",
        environment_path="conf/local/environment.yml",
        credentials_path="conf/local/credentials.yml",
        config_logger=True,
    ) -> None:
        self.root_dir = root_dir
        self.credentials = read_yaml(os.path.join(root_dir, credentials_path))
        self.environment_config = set_environment_config(
            os.path.join(root_dir, environment_path), environment_name
        )

        for key, value in self.environment_config.items():
            setattr(self, key, value)

        if config_logger:
            self.logger = set_logging(self.PROJECT_NAME)
        elif config_logger is False:
            self.logger = None
        else:
            raise ValueError("config_logger must be a boolean value")