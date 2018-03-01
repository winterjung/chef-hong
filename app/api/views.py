from flask import jsonify, request

from app.api import api
from app.api.chatter import chatter, error
from .logger import logger


@api.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify(chatter.home())


@api.route('/message', methods=['POST'])
def message():
    try:
        response = chatter.route(request.json)
    except Exception as exc_info:
        logger.error('error', extra={'info': str(exc_info.value)})
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
