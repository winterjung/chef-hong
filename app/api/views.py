import os

from flask import jsonify, request

from app import sentry
from app.api import api
from app.api.chatter import chatter, error
from app.api.logger import logger


@api.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify(chatter.home())


@api.route('/message', methods=['POST'])
def message():
    try:
        data = request.json
        response = chatter.route(data)
    except Exception as exc_info:
        if os.environ.get('FLASK_ENV') == 'production':
            sentry.captureException()
        logger.exception(
            'error %s',
            data.get('content'),
            extra={'info': str(exc_info)}
        )
        response = error()
    return jsonify(response)


@api.route('/friend', methods=['POST'])
def add_friend():
    return jsonify({'message': 'SUCCESS'})


@api.route('/friend/<key>', methods=['DELETE'])
def block_friend(key):
    return jsonify({'message': 'SUCCESS'})


@api.route('/chat_room/<key>', methods=['DELETE'])
def exit_friend(key):
    return jsonify({'message': 'SUCCESS'})
