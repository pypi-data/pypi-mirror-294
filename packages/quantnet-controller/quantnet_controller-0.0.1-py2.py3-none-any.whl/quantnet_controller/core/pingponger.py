"""
Copyright (c) 2023- ESnet

All rights reserved. This program and the accompanying materials
are made available under the terms of the Eclipse Public License v2.0
and Eclipse Distribution License v1.0 which accompany this distribution.
"""

import logging
import asyncio
import json
from quantnet_controller.core.messaging import RPCPingPongCmdHandler
from quantnet_controller.core.pingpong import PingPong

log = logging.getLogger(__name__)


class PingPonger(RPCPingPongCmdHandler):
    def __init__(self, config, rpcclient, rtype="simulations", key="agentId", **kwargs):
        self._calibration_tasks = []
        RPCPingPongCmdHandler.__init__(self)
        self._rpcclient = rpcclient
        self._rpc_topic_prefix = config.rpc_client_topic

        for h in self.rpcclicmdhandlers:
            self._rpcclient.set_handler(h[0], h[1], h[2])

    async def pingpongThread(self, parameters):
        """ Thread to ping
        """
        remotes = parameters["remotes"]
        for remote in remotes:
            agent = remote

            rs = [r for r in PingPong.list() if r["remote"] == remote]
            if not rs:
                from quantnet_controller.common.utils import generate_uuid
                uid = generate_uuid()
                PingPong.add(id=uid, remote=remote, phase="start", reason="")
            else:
                uid = rs[0]["cal_id"]

            # check if remote exists in DB
            from quantnet_controller.core.node import Node
            try:
                Node.get_node_by_ID(remote)
            except Exception as e:
                log.warn(f"Node {remote} not found in DB: {e}")
                # update
                PingPong.update(id=uid, key="phase", value="done")
                PingPong.update(id=uid, key="reason", value=f"{e}")
                continue

            # send ping message to remtoe
            log.info(f"Sending Ping message to {self._rpc_topic_prefix}/{agent} ")
            generationResp = self._rpcclient.call(
                "pingpong.ping",
                {"name": agent,
                 "params": {"say": "hello"}},
                topic=f"{self._rpc_topic_prefix}/{agent}",
                timeout=15.0
            )
            generationResp = json.loads(await generationResp)
            log.info(f"Received Ping response {generationResp}")
            # update
            PingPong.update(id=uid, key="phase", value="done")
            PingPong.update(id=uid, key="reason", value=f"{generationResp}")

        return

    async def pingpong(self, request, timeout=50.0):
        payload = json.loads(request.payload.serialize())
        type = payload["type"]
        if type == "ping":
            remotes = payload["parameters"]["remotes"]
            parameters = {"remotes": remotes}
            asyncio.create_task(self.pingpongThread(parameters))
            pass
        elif type == "pong":
            return PingPong.list()
        else:
            raise Exception(f"unknown type {type}")
