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
import asyncio

# from quantnet_controller.core.messaging import RPCFunctionCmdHandler

log = logging.getLogger(__name__)


class RPCFunctionCmdHandler:
    def __init__(self):
        """
        RPC command handlers
            (cmd name, handle function, class full path)
        """

        self._clihandlers = [
            ("experiment.submit", self.dummy_response, "quantnet_mq.schema.models.experiment.submit"),
            ("experiment.getState", self.dummy_response, "quantnet_mq.schema.models.experiment.getState"),
            ("experiment.getInfo", self.dummy_response, "quantnet_mq.schema.models.experiment.getInfo"),
            ("experiment.setValue", self.dummy_response, "quantnet_mq.schema.models.experiment.setValue"),
            ("experiment.cleanUp", self.dummy_response, "quantnet_mq.schema.models.experiment.cleanUp"),
        ]

    @property
    def rpcclicmdhandlers(self):
        return self._clihandlers

    def dummy_response(self):
        pass


class FunctionDispatcher(RPCFunctionCmdHandler):
    def __init__(self, config, rpcclient, rtype="function", key="agentId", **kwargs):
        self._function_tasks = []
        RPCFunctionCmdHandler.__init__(self)
        self._rpcclient = rpcclient

        for h in self.rpcclicmdhandlers:
            self._rpcclient.set_handler(h[0], h[1], h[2])

    async def executorThread(self, parameters):
        """function submit process"""
        # exp_id = parameters["exp_id"]
        agent = parameters["agentId"]
        # parameters = parameters["parameters"]

        try:
            response = await self.submit(agent, parameters)
            if response["status"]["code"] != 0:
                raise Exception(f"submit failed: {response['status']['status']}")

        except TimeoutError:
            log.error("function submit requests timeout.")
        except Exception as e:
            log.error(f"function submit request failed: {e}")
        finally:
            """set inactive in DB"""
            pass

        return

    async def startExperiment(self, parameters):
        """start a new experiment process"""
        log.info("processing experiment request")

        params = {
            "id": str(parameters["id"]),
            "agentId": str(parameters["agentId"]),
            "experimentName": str(parameters["experimentName"]),
            "parameters": dict(parameters.expParameters),
        }

        try:
            task = asyncio.create_task(self.executorThread(params))

            # await task
            self._function_tasks.append(task)
        except Exception as e:
            raise Exception(f"submit failed between {params['src']} and {params['dst']}: {e.args}")

    async def submit(self, agent, param, timeout=50.0):
        log.info("Submitting function")
        parameters = [{k: v._value} for k, v in param["parameters"].items()]
        submitResp = await self._rpcclient.call(
            "experiment.submit",
            {"expName": param["experimentName"], "parameters": parameters},
            topic=f"rpc/{agent}",
            timeout=timeout,
        )
        submitResp = json.loads(submitResp)
        return submitResp

    async def setValue(self, agent, param, timeout=50.0):
        log.info("setting parameter")
        submitResp = await self._rpcclient.call("experiment.setValue", param, topic=f"rpc/{agent}", timeout=timeout)
        submitResp = json.loads(submitResp)
        return submitResp

    async def cleanup(self, agent):
        log.info("Starting function cleanup")
        agentClenaup = await self._rpcclient.call("experiment.cleanUp", None, topic=f"rpc/{agent}")
        return json.loads(agentClenaup)
