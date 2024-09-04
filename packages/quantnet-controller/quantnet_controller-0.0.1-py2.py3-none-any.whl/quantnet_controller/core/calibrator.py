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
import asyncio
import json
from quantnet_controller.core.messaging import RPCCalibrationCmdHandler
from quantnet_controller.core.calibration import Calibration

log = logging.getLogger(__name__)


class Calibrator(RPCCalibrationCmdHandler):
    def __init__(self, config, rpcclient, rtype="calibrations", key="agentId", **kwargs):
        self._calibration_tasks = []
        RPCCalibrationCmdHandler.__init__(self)
        self.cal_lights = ["H", "D"]
        self._rpcclient = rpcclient
        self._rpc_topic_prefix = config.rpc_client_topic

        for h in self.rpcclicmdhandlers:
            self._rpcclient.set_handler(h[0], h[1], h[2])

    async def calibrationThread(self, parameters):
        """ Thread to execute calibration process """
        cal_id = parameters["id"]
        src = parameters["src"]
        dst = parameters["dst"]
        power = parameters["power"]
        cal_light = parameters["cal_light"]

        try:
            Calibration.add(id=cal_id, src=src, dst=dst, power=power, light=cal_light)

            srcresp, dstresp = await self.init(src, dst, power)
            if srcresp["status"]["code"] != 0 or dstresp["status"]["code"] != 0:
                raise Exception(
                    f"{Calibrator.calibrationThread.__qualname__} \
                    init failed: {srcresp['status']['status']} {dstresp['status']['status']}"
                )

            Calibration.update(cal_id, key="phase", value="calibrate")
            srcresp, dstresp = await self.calibrate(src, dst, cal_light)
            if srcresp["status"]["code"] != 0 or dstresp["status"]["code"] != 0:
                raise Exception(
                    f"{Calibrator.calibrationThread.__qualname__} \
                    calibrate failed: {srcresp['status']['status']} {dstresp['status']['status']}"
                )

            Calibration.update(cal_id, key="phase", value="cleanup")
            srcresp, dstresp = await self.cleanup(src, dst)
            if srcresp["status"]["code"] != 0 or dstresp["status"]["code"] != 0:
                raise Exception(
                    f"{Calibrator.calibrationThread.__qualname__} \
                    cleanup failed: {srcresp['status']} {dstresp['status']}"
                )

            Calibration.update(cal_id, key="phase", value="done")
        except TimeoutError:
            log.error(f"{Calibrator.calibrationThread.__qualname__}: calibration requests timeout.")
            Calibration.update(cal_id, key="phase", value="failed")
        except Exception as e:
            log.error(f"{Calibrator.calibrationThread.__qualname__}: calibration failed: {e}")
            Calibration.update(cal_id, key="phase", value="failed")
        finally:
            """set inactive in DB"""
            Calibration.delete(cal_id)

        return

    async def startCalibration(self, parameters):
        """ Start a new calibration process """
        log.info("processing  calibration request")

        params = {
            "id": str(parameters["id"]),  # generate_uuid(),
            "src": str(parameters["src"]),
            "dst": str(parameters["dst"]),
            "power": float(parameters["power"]),
            "cal_light": str(parameters["cal_light"]),
        }

        try:
            task = asyncio.create_task(self.calibrationThread(params))

            # await task
            self._calibration_tasks.append(task)
        except Exception as e:
            raise Exception(f"calibraton failed between {params['src']} and {params['dst']}: {e.args}")

        # return "init", params["src"], params["dst"], params["power"], params["cal_light"], params["id"]

    async def getCalibration(self, request, last=False):
        log.info("processing  calibration request")

        if last:
            """get last calibration"""
            # list = list_calibrations(include_deleted=True, order=True)
            list = Calibration.list(include_deleted=True, order=True)
            return list[-1]
        elif request.payload.parameters.get("id"):
            """return existing calibrations with given id"""
            cal_id = str(request.payload.parameters["id"])
            if Calibration.exist(cal_id, include_deleted=True):
                cal = Calibration.get_calibration(cal_id)
                return {
                    "phase": cal["phase"],
                    "src": cal["src"],
                    "dst": cal["dst"],
                    "power": cal["power"],
                    "light": cal["light"],
                    "cal_id": cal_id,
                    "created_at": cal["created_at"],
                }
            else:
                raise Exception(f"calibration not found by id: {cal_id}")
        elif request.payload.parameters.get("src") and request.payload.parameters.get("dst"):
            """return existing calibrations with given src and dst"""
            log.error("Unimplemented calibration query")
            return dict()
        else:
            # return list_calibrations(include_deleted=True)
            return Calibration.list(include_deleted=True)

    async def init(self, src, dst, power, timeout=50.0):
        log.info("Sending Calibration initialization")
        rpc_topic_prefix = self._rpc_topic_prefix
        srcinitResp = asyncio.create_task(self._rpcclient.call(
            "calibration.srcInit", {"power": power}, topic=f"{rpc_topic_prefix}/{src}", timeout=timeout
        ))
        dstinitResp = asyncio.create_task(self._rpcclient.call(
            "calibration.dstInit", None, topic=f"{rpc_topic_prefix}/{dst}", timeout=timeout
        ))
        srcinitResp = json.loads(await srcinitResp)
        dstinitResp = json.loads(await dstinitResp)
        return srcinitResp, dstinitResp

    async def calibrate(self, src, dst, cal_light, timeout=50.0):
        log.info("Sending Calibration")
        rpc_topic_prefix = self._rpc_topic_prefix
        generationResp = self._rpcclient.call(
            "calibration.generation", {"cal_light": cal_light}, topic=f"{rpc_topic_prefix}/{src}", timeout=timeout
        )
        generationResp = json.loads(await generationResp)
        calibrateResp = self._rpcclient.call(
            "calibration.calibration", {"cal_light": cal_light}, topic=f"{rpc_topic_prefix}/{dst}", timeout=timeout
        )
        calibrateResp = json.loads(await calibrateResp)
        return generationResp, calibrateResp

    async def cleanup(self, src, dst, timeout=50.0):
        rpc_topic_prefix = self._rpc_topic_prefix
        log.info("Starting Calibration cleanup")
        srcClenaup = await self._rpcclient.call("calibration.cleanUp", None,
                                                topic=f"{rpc_topic_prefix}/{src}", timeout=timeout)
        dstCleanup = await self._rpcclient.call("calibration.cleanUp", None,
                                                topic=f"{rpc_topic_prefix}/{dst}", timeout=timeout)
        return json.loads(srcClenaup), json.loads(dstCleanup)
