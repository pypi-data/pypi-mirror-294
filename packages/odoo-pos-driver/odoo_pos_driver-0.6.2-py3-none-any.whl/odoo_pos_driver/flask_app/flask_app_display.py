import simplejson
from flask import jsonify, request
from loguru import logger

from ..app import app
from ..interface import interface


@app.route("/hw_proxy/send_text_customer_display", methods=["POST", "PUT"])
@logger.catch
def send_text_customer_display():
    logger.trace("send_text_customer_display()")
    text_to_display = request.json.get("params", {}).get("text_to_display")

    if not text_to_display:
        raise Exception(f"Incorrect argument: '{request.json}'")

    lines = simplejson.loads(text_to_display)
    interface.device_display_task_display_lines(lines)
    return jsonify(jsonrpc="2.0", result=True)
