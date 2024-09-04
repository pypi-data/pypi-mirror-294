import json
import logging

from quantnet_controller.common import exception
from quantnet_controller.core.node import Node

import networkx as nx
from networkx import node_link_data
import quantnet_mq.schema.models as models

logger = logging.getLogger(__name__)


class ResourceManager:
    def __init__(self, rtype="nodes", key="agentId", **kwargs):
        self._topo = None
        self._nodes = None

    def node_loader(self, data=None):
        typ = data["systemSettings"]["type"]
        cls = getattr(models, typ)
        return cls(**data)

    async def handle_register(self, node):
        """ handle registration of node
        """
        if node is None:
            raise Exception(f"{ResourceManager.handle_register.__qualname__}: invalid input parameter")

        logger.info(f'Registering node {node.agentId}')

        if isinstance(node, dict):
            jsobj = node
        else:
            jsobj = json.loads(node.serialize())

        try:
            """ save to DB """
            Node.save(desc=jsobj['payload'])
            logger.info(f'Registering node {node.agentId} succeed.')
        except exception.QuantnetException as e:
            logger.warn(f'Registering node {node.agentId} failed: {e}')
            raise Exception(f"An error occured in {ResourceManager.handle_register.__qualname__}: {e}")

    def get_nodes(self, params: dict):
        try:
            if "id" in params and params["id"] is not None:
                self._nodes = Node.get_node_by_ID(str(params["id"]))
            else:
                self._nodes = Node.list()

            # if not isinstance(self._nodes, dict) or not isinstance(self._nodes, list):
            #     self._nodes = list(self._nodes)

            return self._nodes
        except Exception as e:
            raise Exception(f"An error occured in {ResourceManager.get_nodes.__qualname__}: {params}: {e.args}")

    def build_topology(self):
        color_map = dict()

        def add_node(net, Id, label, group=1, title=None, shape=None, data=None):
            net.add_node(Id, size=20, title=label, group=group,
                         label=label, shape='circle', data=data)

        def add_edge(net, src, dst, title=None, dashes=False, arrows='bottom'):
            net.add_edge(src, dst, weight=2, title=title, dashes=dashes,
                         arrows=arrows, color=color_map.get(title))

        g = nx.MultiDiGraph()

        nodes = Node.list()

        channels = dict()
        for node in nodes:
            n = self.node_loader(node)

            nid = str(n.systemSettings.ID)
            add_node(g, nid, nid)
            # now build a channels map
            channels[nid] = dict()
            if not getattr(n, "channels"):
                logger.error(f"Error: Node {nid} does not have expected channels attribute")
                continue
            for c in n.channels:
                channels[nid][c.ID] = c
        # make edges from channel info
        for k, v in channels.items():
            for cid, c in v.items():
                if c.direction == "out":
                    rid = channels.get(c.neighbor.systemRef)
                    if not rid:
                        logger.warn(f"Warning: {k}: {cid}, could not find remote neighbor \
                        system {c.neighbor.systemRef}")
                        continue
                    rcid = rid.get(c.neighbor.channelRef)
                    if not rcid:
                        logger.warn(f"Warning: {k}: {cid}, could not find remote neighbor channel \
                        {c.neighbor.channelRef}")
                        continue
                    if rcid.direction == "in":
                        add_edge(g, str(k), str(c.neighbor.systemRef), str(c.type))
                    else:
                        logger.error(f"Error: {k}: {cid} out does not match {c.neighbor.systemRef}: {rcid.ID} in")
        self._topo = g

    @property
    def topology(self):
        return node_link_data(self._topo)
