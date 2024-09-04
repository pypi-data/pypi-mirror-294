"""
Main module.
"""
from quantnet_mq.msgserver import MsgServer
from quantnet_mq.rpcserver import RPCServer
from quantnet_mq.rpcclient import RPCClient
from quantnet_controller.core.calibrator import Calibrator
from quantnet_controller.core.simulator import Simulator
from quantnet_controller.core.pingponger import PingPonger
from quantnet_controller.core.scheduler import Scheduler
from quantnet_controller.core.manager import ResourceManager
from quantnet_controller.core.messaging import RPCAgentCmdHandler, TopicHandler
from quantnet_controller.common.config import Config
from quantnet_mq.schema.models import Schema
from typing import Optional
from types import FrameType
import asyncio
import os
import signal
import logging
import uvloop

logger = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class QuantnetServer(RPCAgentCmdHandler, TopicHandler):
    def __init__(self, config: Config) -> None:
        # super(QuantnetServer, self).__init__(config)
        self._scheduler = Scheduler()
        RPCAgentCmdHandler.__init__(self, self._scheduler)
        TopicHandler.__init__(self)
        self.config = config
        self.started = False
        self.should_exit = False
        self.force_exit = False
        self._msgserver = None
        self._rpcserver = None
        self._rm = None
        self._calibrator = None
        self._dispatchers = {}
        self._rpcclient = RPCClient(
            "quantnet_rpcclient", topic="rpc/server", host=config.mq_broker_host, port=config.mq_broker_port
        )
        self.params = {}  # {"stringtest": "value1", "numbertest": 2.1, "integertest": 1}
        logger.info(f"Server started with protocol namespaces:\n{Schema()}")

    def run(self) -> None:
        # self.config.setup_event_loop()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        return asyncio.run(self.serve())

    async def serve(self) -> None:
        process_id = os.getpid()

        # Install signal handlers
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self.handle_exit, signal.SIGINT, None)
            loop.add_signal_handler(signal.SIGTERM, self.handle_exit, signal.SIGTERM, None)
        except NotImplementedError:
            return

        message = "Started server process [%d]"
        logger.info(message % process_id)

        await self.startup()
        if self.should_exit:
            return
        await self.main_loop()
        await self.shutdown()

        message = "Finished server process [%d]"
        logger.info(message % process_id)

    async def startup(self) -> None:
        """ Start up services of all modules """

        # Start Msg Server
        self._msgserver = MsgServer('quantnet_msgserver',
                                    host=self.config.mq_broker_host,
                                    port=self.config.mq_broker_port)
        for h in self.topichandlers:
            self._msgserver.listen(h[0], h[1])
        await self._msgserver.start()

        # Start RPC server
        self._rpcserver = RPCServer("quantnet_rpcserver",
                                    topic=self.config.rpc_server_topic,
                                    host=self.config.mq_broker_host,
                                    port=self.config.mq_broker_port)
        for h in self.rpccmdhandlers:
            self._rpcserver.set_handler(h[0], h[1], h[2])
        await self._rpcserver.start()

        # Start resource manager
        self._rm = ResourceManager(config=self.config)

        # Start calibrator
        self._calibrator = Calibrator(config=self.config, rpcclient=self._rpcclient)

        # Start simulator
        self._simulator = Simulator(config=self.config, rpcclient=self._rpcclient)

        # Start simulator
        self._pingponger = PingPonger(config=self.config, rpcclient=self._rpcclient)

        # Start RPC client
        await self._rpcclient.start()

        # Change the server status
        self.started = True

        # Start scheduler
        self.scheduler.start()

    async def main_loop(self) -> None:
        counter = 0
        should_exit = self.should_exit
        while not should_exit:
            counter += 1
            counter = counter % 864000
            await asyncio.sleep(0.1)
            should_exit = self.should_exit

    async def shutdown(self) -> None:
        logger.info("Shutting down")

        await self._rpcserver.stop()
        await self._msgserver.stop()

    def handle_exit(self, sig: int, frame: Optional[FrameType]) -> None:
        if self.should_exit and sig == signal.SIGINT:
            self.force_exit = True
        else:
            self.should_exit = True
