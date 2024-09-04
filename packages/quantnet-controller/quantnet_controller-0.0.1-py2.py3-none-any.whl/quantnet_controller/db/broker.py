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
import json
import abc
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy.engine import url  # , make_url
from sqlalchemy.orm import exc
from urllib.parse import urlparse
from quantnet_mq.schema.models import QNode, MNode, BSMNode, OpticalSwitch
from quantnet_controller.common.config import config_get
from quantnet_controller.common.utils import generate_uuid
from quantnet_controller.common import exception
from quantnet_controller.db.sqla import models
from quantnet_controller.db.sqla import calibration as Calibration
from quantnet_controller.db.sqla import pingpong as PingPong
from quantnet_controller.db.sqla.constants import NodeType
from quantnet_controller.db.sqla.session import read_session
from quantnet_controller.db.sqla.bsmnode import add_bsmnode, get_bsmnode, list_bsmnodes
from quantnet_controller.db.sqla.qnode import add_qnode, get_qnode, list_qnodes
from quantnet_controller.db.sqla.mnode import add_mnode, get_mnode, list_mnodes
from quantnet_controller.db.sqla.switch import add_switch, get_switch, list_switches
from quantnet_controller.db.nosql.node import (
    save_node as mongo_savenode,
    get_nodes as mongo_getnode,
    list_nodes as mongo_listnodes
)
from quantnet_controller.db.nosql.calibration import (
    add_calibration as mongo_addCalib,
    calibration_exists as mongo_existCalib,
    get_calibration as mongo_getCalib,
    list_calibrations as mongo_listCalib,
    update_calibration as mongo_updateCalib,
    del_calibration as mongo_delCalib
)
from quantnet_controller.db.nosql.pingpong import (
    add_pingpong as mongo_addPingPong,
    pingpong_exists as mongo_existPingPong,
    get_pingpong as mongo_getPingPong,
    list_pingpongs as mongo_listPingPong,
    update_pingpong as mongo_updatePingPong,
    del_pingpong as mongo_delPingPong
)


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from typing import Callable, Optional, ParamSpec, TypeVar
    P = ParamSpec("P")
    R = TypeVar("R")

DATABASE_SECTION = 'database'
__BROKER = None


class BrokerType(Enum):
    SQLA = 'sqla'
    MONGO = 'mongo'


def is_dialect_supported(database_url: str):
    try:
        parsed_url = url.make_url(database_url)
        return parsed_url.get_dialect().name is not None
    except Exception:
        return False


def check_database_type(database_url: str):
    if is_dialect_supported(database_url):
        return BrokerType.SQLA
    elif urlparse(database_url).scheme == "mongodb":
        return BrokerType.MONGO
    else:
        raise Exception(f'{database_url} is not supported')


class Broker(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_nodes(self):
        pass

    @abc.abstractmethod
    def get_nodes(self, ID, **kwargs):
        pass

    @abc.abstractmethod
    def save_node(self, desc, **kwargs):
        pass

    @abc.abstractmethod
    def add_calibration(self, id, src=None, dst=None, power=0.0, light=None):
        pass

    @abc.abstractmethod
    def update_calibration(self, id, key, value):
        pass

    @abc.abstractmethod
    def delete_calibration(self, id):
        pass

    @abc.abstractmethod
    def exist_calibration(self, id, include_deleted):
        pass

    @abc.abstractmethod
    def get_calibration(self, id):
        pass

    @abc.abstractmethod
    def list_calibrations(self, filter_=None, include_deleted=False, order=False):
        pass

    @abc.abstractmethod
    def add_pingpong(self, id, remote=None, phase=None, reason=None):
        pass

    @abc.abstractmethod
    def update_pingpong(self, id, key, value):
        pass

    @abc.abstractmethod
    def list_pingpongs(self, filter_=None, include_deleted=False, order=False):
        pass


class SqlaBroker(Broker):
    def __init__(self, **kwargs):
        self._type = None
        self._output = None
        pass

    @read_session
    def get_nodes(self, ID, *, session: "Session"):
        """Returns a node for the given id.

        :param id: the id of the qnode.
        :param session: the database session in use.

        :returns: a dict with all information for the qnode.
        """

        try:
            query = session.query(models.SystemSetting).\
                filter_by(ID=ID)
            setting = query.first()
        except exc.NoResultFound:
            raise exception.NodeNotFound(f"Qnode with ID '{id}' cannot be found")

        try:
            if setting.type == "QNode":
                device = get_qnode(setting.qnode_id)
            elif setting.type == "MNode":
                device = get_mnode(setting.mnode_id)
            elif setting.type == "BSMNode":
                device = get_bsmnode(setting.bsmnode_id)
            elif setting.type == "OpticalSwitch":
                device = get_switch(setting.switch_id)
            else:
                raise exception.InvalidType(f"Unknown device type: {setting.type}")
        except Exception:
            raise exception.QuantnetException(f"Cannot find device: {ID}")

        return device

    def list_nodes(self):
        return list_qnodes({}) + list_bsmnodes({}) + list_mnodes({}) + list_switches({})

    def save_node(self, desc, **kwargs):
        """ Save the data in desc to database

        :param desc: contain the data to be saved

        :returns: uuid, type, jsobj: the information on the saved data
        """
        if isinstance(desc, QNode):
            type = NodeType.QUANTUM
            jsobj = json.loads(desc.serialize())
        elif isinstance(desc, MNode):
            type = NodeType.M
            jsobj = json.loads(desc.serialize())
        elif isinstance(desc, BSMNode):
            type = NodeType.BSM
            jsobj = json.loads(desc.serialize())
        elif isinstance(desc, OpticalSwitch):
            type = NodeType.SWITCH
            jsobj = json.loads(desc.serialize())
        elif isinstance(desc, dict):
            jsobj = desc
            try:
                type = NodeType(jsobj["systemSettings"]["type"])
            except Exception:
                raise Exception(
                    f"{SqlaBroker.save_node.__qualname__}: Unknown value in the systemSetting.type: \
                         {jsobj['systemSettings']['type']}.")
        else:
            raise exception.InvalidType(f"Invalid type in {SqlaBroker.save_node.__qualname__} arguments.")

        uuid = generate_uuid()
        try:
            if type == NodeType.QUANTUM:
                add_qnode(
                    id=uuid,
                    system_settings=jsobj['systemSettings'],
                    qubit_settings=jsobj['qubitSettings'],
                    interface_settings=jsobj['matterLightInterfaceSettings'],
                    channel_settings=jsobj['channels'])
            elif type == NodeType.SWITCH:
                add_switch(
                    id=uuid,
                    system_settings=jsobj['systemSettings'],
                    channels=jsobj['channels'])
            elif type == NodeType.M:
                add_mnode(
                    id=uuid,
                    system_settings=jsobj['systemSettings'],
                    quantum_settings=jsobj['quantumSettings'],
                    channels=jsobj['channels'])
            elif type == NodeType.BSM:
                add_bsmnode(
                    id=uuid,
                    system_settings=jsobj['systemSettings'],
                    quantum_settings=jsobj['quantumSettings'],
                    channels=jsobj['channels'])
            else:
                raise exception.InvalidType(f"Unknown Node type: {type}")
        except Exception as e:
            raise exception.QuantnetException(e)

        return uuid, type, jsobj

    def read_node(self, uuid):
        """ Return a node with given uuid.

        :param uuid: the uuid of the node

        :returns: a dict with information for the node
        """

        self._output = get_qnode(uuid)
        if not self._output.is_empty():
            self._type = NodeType.QUANTUM
            return self._output

        self._output = get_bsmnode(uuid)
        if not self._output.is_empty():
            self._type = NodeType.BSM
            return self._output

        self._output = get_mnode(uuid)
        if not self._output.is_empty():
            self._type = NodeType.M
            return self._output

        self._output = get_switch(uuid)
        if not self._output.is_empty():
            self._type = NodeType.SWITCH
            return self._output

        return {}

    def add_calibration(self, id, src=None, dst=None, power=0.0, light=None):
        Calibration.add_calibration(id, src, dst, power, light)

    def update_calibration(self, id, key, value):
        Calibration.update_calibration(id, key, value)

    def delete_calibration(self, id):
        Calibration.del_calibration(id)

    def exist_calibration(self, id, include_deleted):
        return Calibration.calibration_exists(id, include_deleted)

    def get_calibration(self, id):
        return Calibration.get_calibration(id)

    def list_calibrations(self, filter_=None, include_deleted=False, order=False):
        return Calibration.list_calibrations(filter_, include_deleted, order)

    def add_pingpong(self, id, remote=None, phase=None, reason=None):
        PingPong.add_pingpong(id, remote, phase, reason)

    def update_pingpong(self, id, key, value):
        PingPong.update_pingpong(id, key, value)

    def list_pingpongs(self, filter_=None, include_deleted=False, order=False):
        return PingPong.list_pingpongs(filter_, include_deleted, order)


class MongoBroker(Broker):
    def __init__(self, **kwargs):
        pass

    def list_nodes(self):
        return mongo_listnodes()

    def get_nodes(self, ID, **kwargs):
        return mongo_getnode(ID)

    def save_node(self, desc, **kwargs):
        return mongo_savenode(desc)

    def add_calibration(self, id, src=None, dst=None, power=0.0, light=None):
        mongo_addCalib(id, src, dst, power, light)

    def update_calibration(self, id, key, value):
        mongo_updateCalib(id, key, value)

    def delete_calibration(self, id):
        mongo_delCalib(id)

    def exist_calibration(self, id, include_deleted):
        return mongo_existCalib(id, include_deleted)

    def get_calibration(self, id):
        return mongo_getCalib(id)

    def list_calibrations(self, filter_=None, include_deleted=False, order=False):
        return mongo_listCalib(filter_, include_deleted, order)

    def add_pingpong(self, id, remote=None, phase=None, reason=None):
        mongo_addPingPong(id, remote, phase, reason)

    def update_pingpong(self, id, key, value):
        mongo_updatePingPong(id, key, value)

    def delete_pingpong(self, id):
        mongo_delPingPong(id)

    def exist_pingpong(self, id, include_deleted):
        return mongo_existPingPong(id, include_deleted)

    def get_pingpong(self, id):
        return mongo_getPingPong(id)

    def list_pingpongs(self, filter_=None, include_deleted=False, order=False):
        return mongo_listPingPong(filter_, include_deleted, order)


def broker(func: "Callable[P, R]"):
    """ Decorate a function that set the broker variable
    """

    def wrapper(*args: "P.args", broker: "Optional[Broker]" = None, **kwargs):
        global __BROKER
        if __BROKER is None:
            url = config_get(DATABASE_SECTION, 'default', check_config_table=False)
            broker_type = check_database_type(url)
            if broker_type == BrokerType.SQLA:
                broker = SqlaBroker()
            elif broker_type == BrokerType.MONGO:
                broker = MongoBroker()
            else:
                raise Exception(f"{url} not implemented")
            __BROKER = broker
        else:
            broker = __BROKER

        return func(*args, broker=broker, **kwargs)
    return wrapper
