
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

from quantnet_controller.db.nosql.db import DBLoader

DATABASE_SECTION = 'database'

_DATABASE = None


def layer(rtype, key):
    """ Decorate a function that set the layer variable
    """
    def inner(func):
        def wrapper(*args, **kwargs):

            global _DATABASE
            if _DATABASE:
                layer = _DATABASE.get_db_layer(rtype, key)
            else:
                _DATABASE = DBLoader(**kwargs)
                layer = _DATABASE.get_db_layer(rtype, key)
            return func(*args, layer, **kwargs)
        return wrapper
    return inner
