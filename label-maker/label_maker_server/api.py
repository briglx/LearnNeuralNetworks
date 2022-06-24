from flask import Blueprint, request, abort
import json

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/test')
def get_test():

    return json.dumps("HELLO API")


@bp.route('/labels/<collection>/<imageId>', methods=['POST', 'GET'])
def get_image_by_id(collection, imageId):

    if not request.json:
        abort(400)

    return json.dumps(request.json)