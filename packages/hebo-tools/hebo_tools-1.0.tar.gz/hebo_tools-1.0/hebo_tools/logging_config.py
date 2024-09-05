# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

# 配置日志格式
LOG_FORMAT = '%(name)s %(asctime)s %(levelname)s %(funcName)s %(lineno)s: %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

# 创建 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 文件处理器配置
file_handler = RotatingFileHandler(filename='app.log', maxBytes=10 * 1024 * 1024, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# 控制台处理器配置
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 添加处理器到 logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
