from logger import Logger

logger = Logger(config_file_path="log_config.json")
logger.info("User login attempt for email user@example.com", user_id="123456789", ssn="123-45-6789", transaction="TX123456")
