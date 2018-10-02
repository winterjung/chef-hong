import os

from logstash_async.handler import AsynchronousLogstashHandler
from logzero import logger as _logger

host = 'localhost'
port = 5959

logger = _logger

if os.environ.get('FLASK_ENV') == 'production':
    handler = AsynchronousLogstashHandler(host, port, None)
    logger.addHandler(handler)
