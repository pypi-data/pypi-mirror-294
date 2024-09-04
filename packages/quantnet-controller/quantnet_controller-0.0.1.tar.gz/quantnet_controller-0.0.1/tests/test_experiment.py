import sys
import json
import asyncio
from quantnet_mq.rpcclient import RPCClient

ret = None


def handle_experiment(request):
    print(f"experiment callback: {request.serialize()}")


async def start_experiment(client, src, param, repeat=5):
    msg = {
        "type": "submit",
        "agentId": src,
        "experimentName": "exp/rabi_flopping.py",
        "expParameters": param,
        "repeat": repeat,
    }
    ret = await client.call("submitExperiment", msg, timeout=5000.0)
    ret = json.loads(ret)
    print(ret)
    return ret["experiments"][0]["exp_id"]


async def list_experiments(client):
    pass


async def get_experiment(client, cid):
    pass


async def main():
    client = RPCClient("experiment-test", host="localhost", port=1884)
    client.set_handler("submitExperiment", handle_experiment, "quantnet_mq.schema.models.submitExperiment")
    await client.start()

    if len(sys.argv) > 1:
        await get_experiment(client, sys.argv[1])
    else:
        cal_id = await start_experiment(client, "agent1", {"param1": "test", "param2": 2})
        await list_experiments(client)
        await get_experiment(client, cal_id)


if __name__ == "__main__":
    asyncio.run(main())
