from flask.wrappers import Response
from flask import jsonify, Blueprint

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index() -> Response:
    return jsonify('OK'), 200


@home.route('/health', methods=['GET'])
def health() -> Response:
    return jsonify(status='ok'), 200
