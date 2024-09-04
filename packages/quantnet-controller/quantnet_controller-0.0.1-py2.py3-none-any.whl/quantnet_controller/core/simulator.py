# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import json
from quantnet_controller.core.messaging import RPCSimulatonCmdHandler

log = logging.getLogger(__name__)


class Simulator(RPCSimulatonCmdHandler):
    def __init__(self, config, rpcclient, rtype="simulations", key="agentId", **kwargs):
        self._calibration_tasks = []
        RPCSimulatonCmdHandler.__init__(self)
        self._rpcclient = rpcclient
        self._rpc_topic_prefix = config.rpc_client_topic

        for h in self.rpcclicmdhandlers:
            self._rpcclient.set_handler(h[0], h[1], h[2])

    async def simulate(self, request, timeout=50.0):
        name = request.payload.parameters.get("name")
        agent = request.payload.parameters.get("src")
        log.info(f"Sending Simulation request to {self._rpc_topic_prefix}/{agent} ")
        generationResp = self._rpcclient.call(
            "simulation.simulate",
            {"name": name,
             "params": {"purpose_id": 4, "number": 4}},
            topic=f"{self._rpc_topic_prefix}/{agent}",
            timeout=timeout
        )
        generationResp = json.loads(await generationResp)
        return generationResp
