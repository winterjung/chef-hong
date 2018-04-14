from flask import jsonify

from app.api.menu import chef
from app.util import util


@util.route('/chef_cache', methods=['GET'])
def chef_cache():
    return jsonify(chef.cache)
