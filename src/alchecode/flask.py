import argparse
import logging

from flask import Flask, request

from alchecode.app import Application
from config import Config
from utils.logger import formatter, logger

app = Flask(Config.app_name)


@app.route("/")
def home() -> dict[str, str]:
    input = (request.get_json(silent=True) or {}).get("input") or request.values.get(
        "input", ""
    )

    if not input:
        return {"error": "Input is required"}

    app = Application(input)
    result = app.run()
    return {"result": result}


def api_server() -> None:
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="AlcheCode API server")
    parser.add_argument(
        "--port",
        type=int,
        default=Config.api_port,
        help=f"Port number (default: {Config.api_port})",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=Config.api_host,
        help=f"Host address (default: {Config.api_host})",
    )

    args = parser.parse_args()

    # 日志处理
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 运行 Flask 应用
    app.run(host=args.host, port=args.port)
