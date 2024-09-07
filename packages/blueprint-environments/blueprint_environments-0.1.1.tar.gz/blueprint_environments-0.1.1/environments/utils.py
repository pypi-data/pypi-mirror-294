import os
from datetime import datetime
import logging
import yaml
import logging.config

def read_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
    
def set_environment_config(file_path, environment_name):
    config = read_yaml(file_path)
    gen_config = config.get("GENERAL", {})
    env_config = config.get(environment_name, {})
    if env_config:
        gen_config.update(env_config)
    else:
        print("error")

    return gen_config

def set_logging(project_name, log_path="logs", versioned_logger = True, log_console = True):
   
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    with open("conf/base/logging.yml", "r") as file:
        config = yaml.safe_load(file)

    if versioned_logger:
        logger_filename = os.path.join(
            log_path,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{project_name}.log",
        )
        config["handlers"]["info_file_handler"]["filename"] = logger_filename

    if not log_console:
        config["root"]["handlers"] = ["info_file_handler"]

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    logger.info("Development Environment Setup successful")
    logger.info("Development Environment Variables Setup succesfully")
    return logger
    