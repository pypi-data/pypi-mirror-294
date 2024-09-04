import sys
import json
import asyncio
from quantnet_mq.rpcclient import RPCClient

ret = None


def handle_calibration(request):
    print(f"calibration callback: {request.serialize()}")


async def start_calibration(client, src, dst, power, repeat=5):
    msg = {"type": "calibrate", "parameters": {"src": src, "dst": dst, "power": power, "cal_light": "H"},
           "repeat": repeat}
    ret = await client.call("calibrate", msg, timeout = 50.0)
    ret = json.loads(ret)
    print(ret)
    return ret['calibrations'][0]['cal_id']


async def list_calibrations(client):
    msg = {"type": "get", "parameters": {}}
    ret = await client.call("calibrate", msg)
    ret = json.loads(ret)
    print(ret)


async def get_calibration(client, cid):
    msg = {"type": "get", "parameters": {'id': cid}}
    ret = await client.call("calibrate", msg)
    ret = json.loads(ret)
    print(ret)


async def main():
    client = RPCClient("calibration-test", host="docker")
    client.set_handler("calibrate", handle_calibration, "quantnet_mq.schema.models.agentCalibration")
    await client.start()

    if len(sys.argv) > 1:
        await get_calibration(client, sys.argv[1])
    else:
        cal_id = await start_calibration(client, "agent1", "agent2", 0.1)
        await list_calibrations(client)
        await get_calibration(client, cal_id)

if __name__ == "__main__":
    asyncio.run(main())
