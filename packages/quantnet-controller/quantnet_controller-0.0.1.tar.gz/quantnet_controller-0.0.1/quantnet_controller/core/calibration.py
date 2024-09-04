from quantnet_controller.db.broker import broker as db_broker, Broker


class Calibration:
    @staticmethod
    @db_broker
    def add(id, src=None, dst=None, power=0.0, light=None, *, broker: Broker, **kwargs) -> str:
        broker.add_calibration(id, src, dst, power, light)

    @staticmethod
    @db_broker
    def update(id, key, value, broker: Broker, **kwargs):
        return broker.update_calibration(id, key, value)

    @staticmethod
    @db_broker
    def delete(id, broker: Broker, **kwargs):
        return broker.delete_calibration(id)

    @staticmethod
    @db_broker
    def exist(id, include_deleted, broker: Broker, **kwargs):
        return broker.exist_calibration(id, include_deleted)

    @staticmethod
    @db_broker
    def get_calibration(id, *, broker: Broker, **kwargs):
        return broker.get_calibration(id)

    @staticmethod
    @db_broker
    def list(*args, broker: Broker, **kwargs):
        return broker.list_calibrations(*args, **kwargs)

    @staticmethod
    @db_broker
    def read(uuid, *, broker: Broker, **kwargs):
        return broker.read_node(uuid)
