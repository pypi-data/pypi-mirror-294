import asyncio
import logging
import os
from time import sleep

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.db.models import AliveBeam
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class Consumer:
    def __init__(self, relay, beams: dict):
        while not relay.beam_pub_key:
            sleep(0.5)
        self.id = relay.beam_pub_key

        asyncio.run(self.mark_ready(False))
        self.beams = beams

        self.client = relay.beam.client

        while not relay.beam.connected:
            logger.debug(f"Consumer waiting for beam {self.id} to connect")
            sleep(0.5)

        asyncio.run(self.mark_ready(True))
        self.start()

    async def mark_ready(self, ready: bool):
        await AliveBeam.mark_beam_ready(self.id, ready)

    def start(self):
        logger.info(f"Consumer subscribed on channel {self.id} PID: {os.getpid()}")

        while True:
            msg = self.beams[self.id][0].recv()
            self.process_message(msg)

    def process_message(self, msg):
        logger.debug(
            f"Consumer {self.id} sending message to {self.client.host}:{self.client.port}")
        self.client.send_message(msg, ack=False)
