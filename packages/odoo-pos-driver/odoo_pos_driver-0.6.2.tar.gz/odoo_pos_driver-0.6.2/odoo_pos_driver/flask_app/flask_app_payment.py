from flask import jsonify, request
from loguru import logger

from ..app import app


@app.route(
    "/hw_proxy/payment_terminal_transaction_start", methods=["POST", "PUT"]
)
@logger.catch
def payment_terminal_transaction_start():
    logger.trace("payment_terminal_transaction_start()")
    payment_info = request.json.get("params", {}).get("payment_info")
    if not payment_info:
        raise Exception(f"Incorrect argument: '{request.json}'")

    logger.warning(
        "TODO: payment_terminal::payment_terminal_transaction_start"
    )
    logger.info(f"payment_info: {payment_info}")
    return jsonify(jsonrpc="2.0", result=True)
