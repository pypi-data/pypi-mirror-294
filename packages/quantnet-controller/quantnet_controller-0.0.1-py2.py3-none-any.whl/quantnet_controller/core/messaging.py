import logging

# import asyncio

from quantnet_mq import Code
from quantnet_mq.schema.models import (
    agentRegisterResponse,
    agentDeregisterResponse,
    agentCalibrationResponse,
    agentSimulationResponse,
    agentPingPongResponse,
    getInfoResponse,
    submitExperimentResponse,
    Status as responseStatus,
)

from quantnet_controller.common.utils import generate_uuid
from quantnet_controller.core.functiondispatcher import FunctionDispatcher

logger = logging.getLogger(__name__)


class RPCAgentCmdHandler:
    def __init__(self, scheduler):
        """
        RPC command handlers
            (cmd name, handle function, class full path)
        """
        self._handlers = [
            ("register", self.handle_register, "quantnet_mq.schema.models.agentRegister"),
            ("deregister", self.handle_deregister, "quantnet_mq.schema.models.agentDeregister"),
            ("update", self.handle_update, "quantnet_mq.schema.models.agentUpdate"),
            ("getinfo", self.handle_getinfo, "quantnet_mq.schema.models.getInfo"),
            ("calibrate", self.handle_calibration, "quantnet_mq.schema.models.agentCalibration"),
            ("simulate", self.handle_simulation, "quantnet_mq.schema.models.agentSimulation"),
            ("submitExperiment", self.handle_experiment, "quantnet_mq.schema.models.submitExperiment"),
            ("pingpong", self.handle_pingpong, "quantnet_mq.schema.models.agentPingPong"),
        ]
        self.scheduler = scheduler

    @property
    def rpccmdhandlers(self):
        return self._handlers

    async def handle_experiment(self, request):
        """handle Experiment submission"""
        logger.info(f"Received experiment: {request.serialize()}")
        rc = 0
        if request.payload.type == "submit":
            expid = generate_uuid()
            agentId = request.payload.agentId
            request.payload["id"] = expid

            if agentId not in self._dispatchers:
                return submitExperimentResponse(
                    status=responseStatus(code=rc, value=Code(rc).name, reason=f"Agent ID : {agentId} not registered")
                )

            await self.scheduler.schedule(self._dispatchers[agentId].startExperiment, request.payload)
            return submitExperimentResponse(
                status=responseStatus(code=rc, value=Code(rc).name),
                experiments=[
                    {
                        "phase": "init",
                        "agentId": request.payload.agentId,
                        "expName": request.payload.experimentName,
                        "param": request.payload.expParameters,
                        "exp_id": expid,
                    }
                ],
            )

        elif request.payload.type == "get":
            exps = await self._calibrator.getExperiment(request)
            exps = [exps] if isinstance(exps, dict) else exps
            return submitExperimentResponse(status=responseStatus(code=rc, value=Code(rc).name), experiments=exps)
        else:
            raise Exception(f"unknown experiment cmd type {request.payload.type}")

    async def handle_calibration(self, request):
        """handle calibration"""
        logger.info(f"Received calibration: {request.serialize()}")
        rc = 0
        if request.payload.type == "calibrate":
            calid = generate_uuid()
            request.payload.parameters["id"] = calid
            await self.scheduler.schedule(self._calibrator.startCalibration, request.payload.parameters)
            return agentCalibrationResponse(
                status=responseStatus(code=rc, value=Code(rc).name),
                calibrations=[
                    {
                        "phase": "init",
                        "src": request.payload.parameters["src"],
                        "dst": request.payload.parameters["dst"],
                        "power": request.payload.parameters["power"],
                        "light": request.payload.parameters["cal_light"],
                        "cal_id": calid,
                    }
                ],
            )
        elif request.payload.type == "get":
            calibs = await self._calibrator.getCalibration(request)
            calibs = [calibs] if isinstance(calibs, dict) else calibs
            return agentCalibrationResponse(status=responseStatus(code=rc, value=Code(rc).name), calibrations=calibs)
        elif request.payload.type == "getLast":
            calibs = await self._calibrator.getCalibration(request, last=True)
            return agentCalibrationResponse(status=responseStatus(code=rc, value=Code(rc).name), calibrations=[calibs])
        else:
            raise Exception(f"unknown calibration type {request.payload.type}")
        pass

    async def handle_simulation(self, request):
        """handle simulation"""
        logger.info(f"Received simulation request: {request.serialize()}")
        rc = 0
        if request.payload.type == "simulate":
            ret = await self._simulator.simulate(request)
            logger.info(ret)
            rc = 0
            return agentSimulationResponse(
                status=responseStatus(code=rc, value=Code(rc).name)
            )
        else:
            raise Exception(f"unknown simulation type {request.payload.type}")
        pass

    async def handle_pingpong(self, request):
        """handle simulation"""
        logger.info(f"Received pingpong request: {request.serialize()}")
        rc = 0
        if request.payload.type == "ping":
            try:
                ret = await self._pingponger.pingpong(request)
            except Exception:
                rc = 6
            return agentPingPongResponse(
                status=responseStatus(code=rc, value=Code(rc).name)
            )
        elif request.payload.type == "pong":
            try:
                ret = await self._pingponger.pingpong(request)
                logger.info(ret)
                return agentPingPongResponse(
                    status=responseStatus(code=rc, value=Code(rc).name), remotes=ret
                )
            except Exception:
                rc = 6
            return agentPingPongResponse(
                status=responseStatus(code=rc, value=Code(rc).name)
            )
        else:
            logger.warn(f"unknown pingpong request type {request.payload.type}")
            rc = 6
            return agentPingPongResponse(
                status=responseStatus(code=rc, value=Code(rc).name))

    def handle_generic(self, request):
        """handle rpc messages"""
        logger.info(f"Received Generic Request: {request.serialize()}")
        return agentRegisterResponse(status={"code": 0, "status": "OK"})

    async def handle_register(self, request):
        """handle rpc messages"""
        logger.info(f"Received Register: {request.serialize()}")

        rc = 0
        try:
            await self.scheduler.schedule(self._rm.handle_register, request)
            dispatcher = FunctionDispatcher(self.config, self._rpcclient)
            self._dispatchers[request.agentId] = dispatcher
            if len(self.params) != 0:
                await dispatcher.setValue(str(request.agentId), self.params)
        except Exception as e:
            rc = 6
            return agentRegisterResponse(status=responseStatus(code=rc, value=Code(rc).name, reason=str(e)))
        return agentRegisterResponse(status=responseStatus(code=rc, value=Code(rc).name))

    def handle_deregister(self, request):
        """handle rpc messages"""
        logger.info(f"Received Deregister: {request.serialize()}")
        rc = 0
        return agentDeregisterResponse(status=responseStatus(code=rc, value=Code(rc).name))

    def handle_update(self, request):
        """handle rpc messages"""
        logger.info(f"Received Update: {request.serialize()}")
        pass

    def handle_getinfo(self, request):
        """handle rpc messages"""
        logger.info(f"Received getInfo: {request.serialize()}")
        rc = 0
        if request.payload.type == "topology":
            self._rm.build_topology()
            return getInfoResponse(status=responseStatus(code=rc, value=Code(rc).name), value=[self._rm.topology])
        elif request.payload.type == "node":
            nodes = self._rm.get_nodes(request.payload.parameters)
            nodes = [nodes] if isinstance(nodes, dict) else nodes
            return getInfoResponse(status=responseStatus(code=rc, value=Code(rc).name), value=nodes)
        else:
            raise Exception(f"unknown type {request.payload.type} in getInfo.")


class RPCCalibrationCmdHandler:
    def __init__(self):
        """
        RPC command handlers
            (cmd name, handle function, class full path)
        """

        self._clihandlers = [
            ("calibration.srcInit", self.dummy_response, "quantnet_mq.schema.models.calibration.srcInit"),
            ("calibration.dstInit", self.dummy_response, "quantnet_mq.schema.models.calibration.dstInit"),
            ("calibration.generation", self.dummy_response, "quantnet_mq.schema.models.calibration.generation"),
            ("calibration.calibration", self.dummy_response, "quantnet_mq.schema.models.calibration.calibration"),
            ("calibration.cleanUp", self.dummy_response, "quantnet_mq.schema.models.calibration.cleanUp"),
        ]

    @property
    def rpcclicmdhandlers(self):
        return self._clihandlers

    def dummy_response(self):
        pass


class RPCPingPongCmdHandler:
    def __init__(self):
        """
        RPC command handlers
            (cmd name, handle function, class full path)
        """

        self._clihandlers = [
            ("pingpong.ping", self.dummy_response, "quantnet_mq.schema.models.pingpong.ping"),
            # ("simulation.collectdata", self.dummy_response, "quantnet_mq.schema.models.simulation.collectdata"),
        ]

    @property
    def rpcclicmdhandlers(self):
        return self._clihandlers

    def dummy_response(self):
        pass


class RPCSimulatonCmdHandler:
    def __init__(self):
        """
        RPC command handlers
            (cmd name, handle function, class full path)
        """

        self._clihandlers = [
            ("simulation.simulate", self.dummy_response, "quantnet_mq.schema.models.simulation.simulation"),
            # ("simulation.collectdata", self.dummy_response, "quantnet_mq.schema.models.simulation.collectdata"),
        ]

    @property
    def rpcclicmdhandlers(self):
        return self._clihandlers

    def dummy_response(self):
        pass


class TopicHandler:
    def __init__(self):
        """
        topic handlers
            (topic name, handle function)
        """
        self._topic_handlers = [
            ("broadcast", self.handle_broadcast, None),
            ("keepalive", self.handle_keepalive, None),
            ("monitoring", self.handle_monitoring, None),
        ]

    @property
    def topichandlers(self):
        return self._topic_handlers

    def handle_broadcast(self, request):
        """handle broadcast topic"""
        logger.debug(f"Received Broadcast: {request}")

        """ TODO: business logic """
        # self.resource_man()
        pass

    def handle_keepalive(self, request):
        """handle keepalive topic"""
        logger.debug(f"Received Keepalive: {request}")

        """ TODO: business logic """
        # self.resource_man()
        pass

    def handle_monitoring(self, request):
        """handle monitoring topic"""
        logger.debug(f"Received Monitoring: {request}")

        """ TODO: business logic """
        # self.resource_man()
        pass
