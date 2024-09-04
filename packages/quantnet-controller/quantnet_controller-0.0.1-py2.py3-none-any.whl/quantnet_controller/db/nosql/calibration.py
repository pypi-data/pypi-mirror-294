from datetime import datetime
from quantnet_controller.db.nosql.layer import layer


@layer(rtype="calibrations", key="agentId")
def add_calibration(id, src, dst, power, light, layer, *args, **kwargs):
    try:
        data = {
            "id": id,
            "src": src,
            "dst": dst,
            "power": power,
            "light": light,
            "phase": "init",
            "created_at": str(datetime.utcnow())
        }
        layer.insert(data)
    except Exception:
        raise


@layer(rtype="calibrations", key="agentId")
def calibration_exists(id, include_deleted, layer, *args, **kwargs):
    """ Checks to see if a calibration exists.

    :param id: ID of the calibration.

    :returns: True if found, otherwise false.
    """
    return True if layer.find_one({"id": id}) else False


@layer(rtype="calibrations", key="agentId")
def get_calibration(id, layer, *args, **kwargs):
    """ Returns an calibration for the given id.

    :param id: the id of the calibration.

    :returns: a dict with all information for the calibration.
    """
    return layer.find_one({"id": id})


@layer(rtype="calibrations", key="agentId")
def del_calibration(id, layer, *args, **kwargs):
    """ Disable a calibration with the given id.

    :param id: the calibration id.
    """
    layer.update({"id": id}, {"deleted_at": str(datetime.utcnow())})


@layer(rtype="calibrations", key="agentId")
def update_calibration(id, key, value, layer, *args, **kwargs):
    """ Update a property of a calibration.

    :param id: ID of the calibration.
    :param key: calibration property like status.
    :param value: Property value.
    """
    layer.update({"id": id}, {key: value})


@layer(rtype="calibrations", key="agentId")
def list_calibrations(filter_, include_deleted, order, layer, *args, **kwargs):
    """ Returns a list of all calibration names.

    :param filter_: Dictionary of attributes by which the input data should be filtered

    returns: a list of all calibration names.
    """
    calibs = layer.find({})
    calibration_list = []
    for cal in calibs:
        calibration_list.append(cal)

    return calibration_list
