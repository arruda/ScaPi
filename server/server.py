#!/usr/bin/env python
"""
Simple Redis server using a Pub/sub comunication, and JSON for the messages serialization.
"""
import json
import logging

import logzero
import redis

from conf import REDIS_ADDRESS, REDIS_PORT, LOGGING_LEVEL


class ScapiServer():
    def __init__(self, redis_address, redis_port, logging_level):
        self.redis_db = redis.Redis(host=redis_address, port=redis_port)
        self.logging_level = logging_level
        self.logger = self._setup_logging()

    def _setup_logging(self):
        log_format = (
            '%(color)s[%(levelname)1.1s %(name)s %(asctime)s:%(msecs)d '
            '%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        )
        formatter = logzero.LogFormatter(fmt=log_format)
        return logzero.setup_logger(
            name=self.__class__.__name__, level=logging.getLevelName(self.logging_level), formatter=formatter)

    def process_msg(self, json_msg):
        msg_data = json.loads(json_msg)
        self.logger.debug(msg_data)

    def run(self):
        pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('scapi')
        for message in pubsub.listen():
            try:
                self.process_msg(message['data'].decode('utf-8'))
            except Exception as e:
                self.logger.error(f'Error processing {message}:')
                self.logger.exception(e)


if __name__ == '__main__':
    scapi_server = ScapiServer(
        redis_address=REDIS_ADDRESS, redis_port=REDIS_PORT,
        logging_level=LOGGING_LEVEL
    )
    scapi_server.run()
