from datetime import datetime
from quantnet_controller.db.nosql.layer import layer


@layer(rtype="pingpong", key="agentId")
def add_pingpong(id, remote, phase, reason, layer, *args, **kwargs):
    try:
        data = {
            "id": id,
            "remote": remote,
            "phase": phase,
            "cal_id": id,
            "reason": reason,
            "created_at": str(datetime.utcnow())
        }
        layer.insert(data)
    except Exception:
        raise


@layer(rtype="pingpong", key="agentId")
def pingpong_exists(id, include_deleted, layer, *args, **kwargs):
    """ Checks to see if a pingpong exists.

    :param id: ID of the pingpong.

    :returns: True if found, otherwise false.
    """
    return True if layer.find_one({"id": id}) else False


@layer(rtype="pingpong", key="agentId")
def get_pingpong(id, layer, *args, **kwargs):
    """ Returns an pingpong for the given id.

    :param id: the id of the pingpong.

    :returns: a dict with all information for the pingpong.
    """
    return layer.find_one({"id": id})


@layer(rtype="pingpong", key="agentId")
def del_pingpong(id, layer, *args, **kwargs):
    """ Disable a pingpong with the given id.

    :param id: the pingpong id.
    """
    layer.update({"id": id}, {"deleted_at": str(datetime.utcnow())})


@layer(rtype="pingpong", key="agentId")
def update_pingpong(id, key, value, layer, *args, **kwargs):
    """ Update a property of a pingpong.

    :param id: ID of the pingpong.
    :param key: pingpong property like status.
    :param value: Property value.
    """
    layer.update({"id": id}, {key: value})


@layer(rtype="pingpong", key="agentId")
def list_pingpongs(filter_, include_deleted, order, layer, *args, **kwargs):
    """ Returns a list of all pingpong names.

    :param filter_: Dictionary of attributes by which the input data should be filtered

    returns: a list of all pingpong names.
    """
    calibs = layer.find({})
    pingpong_list = []
    for cal in calibs:
        pingpong_list.append(cal)

    return pingpong_list
