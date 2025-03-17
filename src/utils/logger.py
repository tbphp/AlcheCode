import logging

logger = logging.getLogger()
"""日志"""
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)-8s%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
