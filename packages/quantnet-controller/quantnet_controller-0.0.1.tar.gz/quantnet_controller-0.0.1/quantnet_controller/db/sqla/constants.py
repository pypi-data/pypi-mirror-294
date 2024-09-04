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

from datetime import datetime
from enum import Enum

# Individual constants

OBSOLETE = datetime(year=1970, month=1, day=1)  # Tombstone value to mark obsolete replicas


# The enum values below are the actual strings stored in the database -- these must be string types.
# This is done explicitly via values_callable to SQLAlchemy enums in models.py and alembic scripts,
# as overloading/overriding Python internal enums is discouraged.


class NodeStatus(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class NodeType(Enum):
    NORMAL = 'NORMAL'
    QUANTUM = "QNode"
    BSM = "BSMNode"
    M = "MNode"
    SWITCH = 'OpticalSwitch'
