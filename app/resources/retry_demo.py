import random
from flask import Blueprint, jsonify

retry_bp = Blueprint("retry", __name__)

@retry_bp.route("/unstable")
def unstable():
    if random.random() < 0.5:
        # simulamos un error del backend
        return jsonify({"ok": False, "source": "backend", "error": "fail random"}), 500
    return jsonify({"ok": True, "source": "backend"}), 200
