from flask import jsonify

from app import sentry
from app.api.menu import chef
from app.util import util


@util.route('/chef_cache', methods=['GET'])
def chef_cache():
    return jsonify(chef.cache)


@util.route('/sentry_test', methods=['GET'])
def test_sentry():
    try:
        msg = int('abs')
    except Exception as exc_info:
        sentry.captureException()
        msg = str(exc_info)
    return jsonify({'msg': msg})
