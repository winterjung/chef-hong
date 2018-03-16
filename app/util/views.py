from flask import jsonify

from app.util import util
from app.api.menu import chef


@util.route('/chef_cache', methods=['GET'])
def chef_cache():
    return jsonify(chef.cache)
