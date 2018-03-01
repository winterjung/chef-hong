import logging
from logstash_async.handler import AsynchronousLogstashHandler

host = 'localhost'
port = 5959

logger = logging.getLogger('chef-hong-logger')
logger.setLevel(logging.INFO)

handler = AsynchronousLogstashHandler(host, port, None)
logger.addHandler(handler)
