"""Console script for quantnet_controller."""
import sys
import click
import asyncio

from quantnet_controller.common.logging import setup_logging
from quantnet_controller.server import QuantnetServer as Quantnet
from quantnet_controller.client.client import QuantnetClient
from quantnet_controller.common.config import Config

STARTUP_FAILURE = 3

STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


@click.command(help="Quantnet Controller")
@click.option(
    "--mq-broker-host",
    "mq_broker_host",
    type=str,
    help="Reach message queue broker to this host.",
    show_default=True,
)
@click.option(
    "--mq-broker-port",
    "mq_broker_port",
    type=int,
    help="Reach message queue broker to this port.",
    show_default=True,
)
@click.option(
    "--mq-mongo-host",
    "mq_mongo_host",
    type=str,
    help="Reach message queue broker to this host.",
    show_default=True,
)
@click.option(
    "--mq-mongo-port",
    "mq_mongo_port",
    type=int,
    help="Reach message queue broker to this port.",
    show_default=True,
)
@click.option(
    "--mode",
    "mode",
    type=str,
    default="server",
    help="Run as QuantNet Server or Client.",
    show_default=True,
)
def main(
    mq_broker_host,
    mq_broker_port,
    mq_mongo_host,
    mq_mongo_port,
    mode,
) -> None:
    run(
        mq_broker_host,
        mq_broker_port,
        mq_mongo_host,
        mq_mongo_port,
        mode,
    )


def run(
    mq_broker_host,
    mq_broker_port,
    mq_mongo_host,
    mq_mongo_port,
    mode
) -> None:
    # Create config
    config = Config(
        mq_broker_host=mq_broker_host,
        mq_broker_port=mq_broker_port,
        mq_mongo_host=mq_mongo_host,
        mq_mongo_port=mq_mongo_port,
    )

    setup_logging()

    if mode == "server":
        # Create and start quantnet
        quantnet = Quantnet(config)
        quantnet.run()

        # Exit if failed
        if not quantnet.started:
            sys.exit(STARTUP_FAILURE)
    elif mode == "client":
        quantclient = QuantnetClient(config)
        quantclient.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
