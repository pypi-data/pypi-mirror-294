===================
quant-net server
===================


.. image:: https://img.shields.io/pypi/v/quantnet_controller.svg
        :target: https://pypi.python.org/pypi/quantnet_controller

.. image:: https://img.shields.io/travis/lzhang9/quantnet_controller.svg
        :target: https://travis-ci.com/lzhang9/quantnet_controller

.. image:: https://readthedocs.org/projects/quantnet-controller/badge/?version=latest
        :target: https://quantnet-controller.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




The server controlling Quant-Net by ESnet


* Free software: MIT license
* Documentation: https://quantnet-controller.readthedocs.io.

Development Install
-------------------

After downloading the source tree, pull requirements and install package in edit mode::

  pip3 install -r requirements.txt
  pip3 install -e .

The `quantnet_controller` script will be available in your local path, or check `~/.local/bin`::

 $ quantnet_controller --help
 Usage: quantnet_controller [OPTIONS]

   Quantnet Controller

 Options:
   --mq-broker-host TEXT     Reach message queue broker to this host.
                             [default: 127.0.0.1]
   --mq-broker-port INTEGER  Reach message queue broker to this port.
                             [default: 1883]
   --mode TEXT               Run as QuantNet Server or Client.  [default:
                             server]
   --help                    Show this message and exit.


Local Development Enviroment
-----------------------------

Docker is used for setting up the local development enviroment such as the Mosquitto server, database server and etc::

    $ cd etc/docker/dev
    $ docker compose up -d

Configuration File
------------------

The configuration file ``quantnet.cfg`` should be created in the path either ``$QUANTNET_HOME/etc/`` or ``/etc/``. A sample is shown::


    [common]
    logdir = /var/log/quantnet
    loglevel = INFO

    [mq]
    rpc_server_topic=rpc/+

    [database]
    default = postgresql://server:secret@localhost/quantnet
    schema = dev
    echo=0
    pool_recycle=3600
    pool_size=20
    max_overflow=20
    pool_reset_on_return=rollback

Bootstrap
---------
The database is initialized by the script::

    tools/bootstrap.py
    
    
Example usage
-------------
An MQTT broker should be available for the agent to connect to. A development docker-compose file that starts an Eclipse Mosquitto instance is available in `quant-net-server:etc/docker/dev`

An example Controller configuration file is available in `quant-net-server:etc/quantnet.cfg`.  This file is optional at the moment.

Running the controller::

 quantnet_controller --mq-broker-host <broker>

