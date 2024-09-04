from quantnet_controller.db.broker import broker as db_broker, Broker


class PingPong:
    @staticmethod
    @db_broker
    def add(id, remote=None, phase=None, reason=None, *, broker: Broker, **kwargs) -> str:
        broker.add_pingpong(id, remote, phase, reason)

    @staticmethod
    @db_broker
    def update(id, key, value, broker: Broker, **kwargs):
        return broker.update_pingpong(id, key, value)

    @staticmethod
    @db_broker
    def delete(id, broker: Broker, **kwargs):
        return broker.delete_pingpong(id)

    @staticmethod
    @db_broker
    def exist(id, include_deleted, broker: Broker, **kwargs):
        return broker.exist_pingpong(id, include_deleted)

    @staticmethod
    @db_broker
    def get_pingpong(id, *, broker: Broker, **kwargs):
        return broker.get_pingpong(id)

    @staticmethod
    @db_broker
    def list(*args, broker: Broker, **kwargs):
        return broker.list_pingpongs(*args, **kwargs)

    @staticmethod
    @db_broker
    def read(uuid, *, broker: Broker, **kwargs):
        return broker.read_node(uuid)
