from flask import jsonify
from loguru import logger

from ..app import app


@app.route("/hw_proxy/scale_read", methods=["POST", "PUT"])
@logger.catch
def scale_read():
    logger.trace("scale_read()")
    logger.warning("TODO: scale::scale_read")
    result = {
        "weight": 12.456,
    }
    return jsonify(jsonrpc="2.0", result=result)
