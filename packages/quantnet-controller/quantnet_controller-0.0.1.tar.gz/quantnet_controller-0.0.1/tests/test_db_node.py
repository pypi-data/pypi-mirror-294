#!/usr/bin/env python3

import logging
import unittest
# import asyncio
import json
# from time import sleep

from quantnet_controller.core.node import Node
# from quantnet_controller.common.utils import generate_uuid
# from quantnet_controller.db.sqla.constants import NodeStatus, NodeType


class TestQnode(unittest.IsolatedAsyncioTestCase):
    logger = logging.getLogger(__name__)
    log_format = \
        '%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - [%(threadName)s] - %(levelname)s - %(message)s'
    logging.basicConfig(handlers=[logging.StreamHandler()], format=log_format, force=True)

    # async def test_add_node_with_system_setttings(self):
    #     systemSetting = {
    #         "type": "Q-node",
    #         "name": "q-node1.lbl.gov",
    #         "ID": "3C-3B-BB-CE-34-6B",
    #         "controlInterface": "10.0.0.3",
    #         "queue": "rpc/QN-server",
    #         "mode": "daemon",
    #         "threads": 3,
    #         "workers": 3}
    #
    #     id = generate_uuid()
    #     add_qnode(id=id, system_settings=systemSetting)
    #     assert(qnode_exists(id))
    #
    #     qnode = get_qnode(id)
    #     print(json.dumps(qnode, indent = 4, sort_keys=False))
    #     assert(qnode['systemSettings'] == systemSetting)
    #
    #     del_qnode(id)
    #
    # async def test_add_node_with_qubits_setttings(self):
    #
    #     qubitSettings = {
    #       "qubits": [
    #         {
    #           "ID": "1",
    #           "quantumObject": "trapped_ion",
    #           "T1": "1.5s",
    #           "T2": "1.1s",
    #           "type": "communication"
    #         },
    #         {
    #           "ID": "2",
    #           "quantumObject": "trapped_ion",
    #           "T1": "1.5s",
    #           "T2": "1.1s",
    #           "type": "communication"
    #         }
    #       ],
    #       "operations": {
    #         "oneQubitGates": [
    #           {
    #             "gate": "rot_x",
    #             "qubits": ["1", "2"]
    #           },
    #           {
    #             "gate": "rot_y",
    #             "qubits": ["1", "2"]
    #           },
    #           {
    #             "gate": "rot_z",
    #             "qubits": ["1", "2"]
    #           }
    #         ],
    #         "twoQubitGates": [
    #           {
    #             "gate": "cnot",
    #             "qubits": ["1" , "2"]
    #           },
    #           {
    #             "gate": "cphase",
    #             "qubits": ["1" , "2"]
    #           }
    #         ]
    #       }
    #     }
    #
    #     id = generate_uuid()
    #     add_qnode(id, qubit_settings=qubitSettings)
    #     assert(qnode_exists(id))
    #
    #     qnode = get_qnode(id)
    #     print(json.dumps(qnode, indent = 4, sort_keys=False))
    #     assert(qnode['qubitSettings'] == qubitSettings)
    #
    #     del_qnode(id)

    # async def test_add_node_with_interface_setttings(self):
    #
    #     matterLightInterfaceSettings = [
    #       {
    #         "name": "Interface 1",
    #         "interface": "1",
    #         "entanglement": {
    #           "type": "∣Φ+⟩",
    #           "rate": "1000 Hz"
    #         },
    #         "flyingQubit": {
    #           "type": "polarization",
    #           "frequency": "1550nm"
    #         },
    #         "channels": [
    #           {
    #                 "ID": "1",
    #                 "name": "channel_1",
    #                 "type": "quantum",
    #                 "direction": "out",
    #                 "wavelength": "1550 nm",
    #                 "power": 12.1,
    #                 "neighbor": {
    #                     "idRef": "urn:quant-net:LBNL-BSM:alice:4",
    #                     "systemRef": "LBNL-BSM",
    #                     "channelRef": "4",
    #                     "loss": "5dB"
    #                 }
    #           },
    #           {
    #               "ID": "2",
    #               "name": "channel_2",
    #               "type": "classic_clk",
    #               "direction": "in",
    #               "wavelength": "1520 nm",
    #               "power": -3.2,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:3",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "3",
    #                 "loss": "5dB"
    #               }
    #           },
    #           {
    #               "ID": "3",
    #               "name": "channel_3",
    #               "type": "classic_bsm_result",
    #               "direction": "in",
    #               "wavelength": "1530 nm",
    #               "power": -4.7,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:2",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "2",
    #                 "loss": "5dB"
    #               }
    #           },
    #           {
    #               "ID": "4",
    #               "name": "channel_4",
    #               "type": "classic_photon_gen",
    #               "direction": "in",
    #               "wavelength": "1540 nm",
    #               "power": -3.2,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:1",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "1",
    #                 "loss": "5dB"
    #               }
    #           }
    #         ]
    #       }
    #     ]
    #
    #     id = generate_uuid()
    #     add_qnode(id, interface_settings=matterLightInterfaceSettings)
    #     assert(qnode_exists(id))
    #
    #     qnode = get_qnode(id)
    #     print(json.dumps(qnode, indent = 4, sort_keys=False))
    #     assert(qnode['matterLightInterfaceSettings'] == matterLightInterfaceSettings)
    #

    # del_qnode(id)

    # async def test_add_node(self):
    #     systemSetting = {
    #         "type": "Q-node",
    #         "name": "q-node1.lbl.gov",
    #         "ID": "3C-3B-BB-CE-34-6B",
    #         "controlInterface": "10.0.0.3",
    #         "mode": "daemon",
    #         "threads": 3,
    #         "workers": 3}
    #
    #     qubitSettings = {
    #       "qubits": [
    #         {
    #           "ID": "1",
    #           "quantumObject": "trapped_ion",
    #           "T1": "1.5s",
    #           "T2": "1.1s",
    #           "type": "communication"
    #         },
    #         {
    #           "ID": "2",
    #           "quantumObject": "trapped_ion",
    #           "T1": "1.5s",
    #           "T2": "1.1s",
    #           "type": "communication"
    #         }
    #       ],
    #       "operations": {
    #         "oneQubitGates": [
    #           {
    #             "gate": "rot_x",
    #             "qubits": ["1", "2"]
    #           },
    #           {
    #             "gate": "rot_y",
    #             "qubits": ["1", "2"]
    #           },
    #           {
    #             "gate": "rot_z",
    #             "qubits": ["1", "2"]
    #           }
    #         ],
    #         "twoQubitGates": [
    #           {
    #             "gate": "cnot",
    #             "qubits": ["1" , "2"]
    #           },
    #           {
    #             "gate": "cphase",
    #             "qubits": ["1" , "2"]
    #           }
    #         ]
    #       }
    #     }
    #
    #     matterLightInterfaceSettings = [
    #       {
    #         "name": "Interface 1",
    #         "interface": "1",
    #         "entanglement": {
    #           "type": "∣Φ+⟩",
    #           "rate": "1000 Hz"
    #         },
    #         "flyingQubit": {
    #           "type": "polarization",
    #           "frequency": "1550nm"
    #         },
    #         "channels": [
    #           {
    #                 "ID": "1",
    #                 "name": "channel_1",
    #                 "type": "quantum",
    #                 "direction": "out",
    #                 "wavelength": "1550 nm",
    #                 "power": 12.1,
    #                 "neighbor": {
    #                     "idRef": "urn:quant-net:LBNL-BSM:alice:4",
    #                     "systemRef": "LBNL-BSM",
    #                     "channelRef": "4",
    #                     "loss": "5dB"
    #                 }
    #           },
    #           {
    #               "ID": "2",
    #               "name": "channel_2",
    #               "type": "classic_clk",
    #               "direction": "in",
    #               "wavelength": "1520 nm",
    #               "power": -3.2,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:3",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "3",
    #                 "loss": "5dB"
    #               }
    #           },
    #           {
    #               "ID": "3",
    #               "name": "channel_3",
    #               "type": "classic_bsm_result",
    #               "direction": "in",
    #               "wavelength": "1530 nm",
    #               "power": -4.7,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:2",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "2",
    #                 "loss": "5dB"
    #               }
    #           },
    #           {
    #               "ID": "4",
    #               "name": "channel_4",
    #               "type": "classic_photon_gen",
    #               "direction": "in",
    #               "wavelength": "1540 nm",
    #               "power": -3.2,
    #               "neighbor": {
    #                 "idRef": "urn:quant-net:LBNL-BSM:alice:1",
    #                 "systemRef": "LBNL-BSM",
    #                 "channelRef": "1",
    #                 "loss": "5dB"
    #               }
    #           }
    #         ]
    #       }
    #     ]
    #
    #     id = generate_uuid()
    #     add_qnode(id,
    #               system_settings=systemSetting,
    #               qubit_settings=qubitSettings,
    #               interface_settings=matterLightInterfaceSettings)
    #     assert(qnode_exists(id))
    #
    #     qnode = get_qnode(id)
    #     print(json.dumps(qnode, indent = 4, sort_keys=False))
    # assert(qnode['matterLightInterfaceSettings'] == matterLightInterfaceSettings)

    # del_qnode(id)

    # async def test_get(self):
    #     id = generate_uuid()
    #     name = 'myqnode'
    #     qnode.add_qnode(id, name)
    #     qn = qnode.get_qnode(id)
    #     assert(qn)
    #     qnode.del_qnode(id)
    #
    # async def test_update(self):
    #     id = generate_uuid()
    #     name = 'myqnode'
    #     qnode.add_qnode(id, name)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.ACTIVE
    #     qnode.update_qnode(id, key='status', value=NodeStatus.SUSPENDED)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.SUSPENDED
    #     qnode.update_qnode(id, key='status', value=NodeStatus.ACTIVE)
    #     assert qnode.get_qnode(id)['status'] == NodeStatus.ACTIVE
    #     qnode.del_qnode(id)

    async def test_list(self):
        # id = generate_uuid()
        # name = 'myqnode'
        try:
            nodes = Node().list()
        except Exception as e:
            raise e
        for n in nodes:
            print(json.dumps(n, indent=4, sort_keys=False))
    #     assert qlist
    # qnode.del_qnode(id)

    async def test_get_node_by_ID(self):

        try:
            device = Node().get_node_by_ID(ID="LBNL-Q")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))

        try:
            device = Node().get_node_by_ID(ID="UCB-Q")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))

        try:
            device = Node().get_node_by_ID(ID="LBNL-M")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))

        try:
            device = Node().get_node_by_ID(ID="UCB-M")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))
        try:
            device = Node().get_node_by_ID(ID="LBNL-BSM")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))
        try:
            device = Node().get_node_by_ID(ID="LBNL-SWITCH")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))

        try:
            device = Node().get_node_by_ID(ID="UCB-SWITCH")
        except Exception as e:
            raise e
        print(json.dumps(device, indent=4, sort_keys=False))
