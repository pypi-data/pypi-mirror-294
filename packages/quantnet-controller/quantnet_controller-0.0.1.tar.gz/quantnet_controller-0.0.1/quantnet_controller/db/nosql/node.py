
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

from quantnet_controller.db.nosql.layer import layer


@layer(rtype="nodes", key="agentId")
def save_node(data, layer, *args, **kwargs):
    try:
        nodes = layer.insert(data)
    except Exception:
        raise

    list = [(node.upserted_id, None, None) for node in nodes]
    return list[0]


@layer(rtype="nodes", key="agentId")
def list_nodes(layer, *args, **kwargs):
    try:
        nodes = layer.find({})
        list = [node for node in nodes]
        return list
    except Exception:
        raise


@layer(rtype="nodes", key="agentId")
def get_nodes(ID, layer, *args, **kwargs):
    try:
        nodes = layer.find({})
        for node in nodes:
            if "systemSettings" in node.keys():
                if node['systemSettings']['ID'] == ID:
                    return node
        return {}
    except Exception:
        raise
