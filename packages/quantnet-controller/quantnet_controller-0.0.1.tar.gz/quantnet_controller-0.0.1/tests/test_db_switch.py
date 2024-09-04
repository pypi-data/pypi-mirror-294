#!/usr/bin/env python3

import os
import logging
import unittest
# import asyncio
import json
import quantnet_mq.schema
from quantnet_controller.common.config import config_get
from quantnet_controller.common.utils import generate_uuid
from quantnet_controller.db.sqla.switch import add_switch, switch_exists, get_switch, list_switches  # , del_switch
# from quantnet_controller.db.sqla.constants import NodeStatus, NodeType

use_sqla = True if "sql" in config_get("database", "default") else False

NODE_PATH = os.path.normpath(
    os.path.join(quantnet_mq.schema.__path__[0],
                 "examples/topology"))

NODES = ["conf_lbnl-switch.json",
         "conf_ucb-switch.json"]

logger = logging.getLogger(__name__)
log_format = \
    '%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - [%(threadName)s] - %(levelname)s - %(message)s'
logging.basicConfig(handlers=[logging.StreamHandler()], format=log_format, force=True)


class TestSwitch(unittest.IsolatedAsyncioTestCase):

    @unittest.skipUnless(use_sqla, "Skipping this test unless use_sqla is True")
    async def test_add_switch(self):

        for node in NODES:
            id = generate_uuid()
            fname = os.path.join(NODE_PATH, node)
            fp = open(fname)
            data = json.load(fp)

            add_switch(id=id,
                       system_settings=data['systemSettings'],
                       channels=data['channels'])
            assert(switch_exists(id))

            switch = get_switch(id)
            print(json.dumps(switch, indent=4, sort_keys=False))

            # del_switch(id)

    # @unittest.skipUnless(use_sqla, "Skipping this test unless use_sqla is True")
    # async def test_get(self):
    #     id = generate_uuid()
    #     name = 'myqnode'
    #     qnode.add_switch(id, name)
    #     qn = qnode.get_qnode(id)
    #     assert(qn)
    #     qnode.del_qnode(id)
    #
    # @unittest.skipUnless(use_sqla, "Skipping this test unless use_sqla is True")
    # async def test_update(self):
    #     id = generate_uuid()
    #     name = 'myqnode'
    #     qnode.add_switch(id, name)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.ACTIVE
    #     qnode.update_qnode(id, key='status', value=NodeStatus.SUSPENDED)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.SUSPENDED
    #     qnode.update_qnode(id, key='status', value=NodeStatus.ACTIVE)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.ACTIVE
    #     qnode.del_qnode(id)

    @unittest.skipUnless(use_sqla, "Skipping this test unless use_sqla is True")
    async def test_list_switch(self):
        try:
            switches = list_switches({})
        except Exception:
            assert(False)
        for switch in switches:
            print(json.dumps(switch, indent=4, sort_keys=False))
