import logging
import os
from datetime import datetime

logger = logging.getLogger()
"""日志实例"""

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)-8s%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger.setLevel(logging.INFO)

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/../../", "logs")
os.makedirs(logs_dir, exist_ok=True)
log_filename = f"app_{datetime.now().strftime('%Y_%m_%d')}.log"
log_file_path = os.path.join(logs_dir, log_filename)

handler = logging.FileHandler(log_file_path)
handler.setFormatter(formatter)
logger.addHandler(handler)
