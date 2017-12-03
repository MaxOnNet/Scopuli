#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2017] Tatarnikov Viktor [viktor@tatarnikov.org]
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

import sys
import os
import threading
import warnings
import logging
import logging.handlers
import time

reload(sys)

sys.setdefaultencoding('utf8')
warnings.simplefilter('ignore', Warning)

log = logging.getLogger(__name__)

import Console.Logging.Colorer

from Interfaces import Config

#   Twisted
from twisted.internet import reactor, defer, protocol
from twisted.internet import reactor as reactor2
from twisted.web.server import Site

#   Stratum
from Interfaces.Stratum.socket_transport import SocketTransportFactory, SocketTransportClientFactory
from Interfaces.Stratum.services import ServiceEventHandler
from Interfaces.Stratum.custom_exceptions import TransportException

#   Proxy
from Interfaces.Proxy.ClientMiningService import ProxyClientMiningService
from Interfaces.Proxy.JobRegistry import ProxyJobRegistry
from Interfaces.Proxy.StratumService import ProxyStratumService, ProxyMiningSubscription


class Scopuli():
    def __init__(self):
        self.config = Config()

        self._pidfile_write()
        self._logging_init()
        self._pools_connect()

    def _logging_init(self):
        threading.current_thread().name = 'main'
    
        logging.basicConfig(level=int(self.config.get("logging", "console", "level", "10")), stream=sys.stdout,
                            format='%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s')
    
        log_handler_console = logging.StreamHandler()
        log_handler_console.setLevel(int(self.config.get("logging", "console", "level", "10")))
        log_handler_console.setFormatter(
            logging.Formatter('%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
    
        if bool(int(self.config.get("logging", "", "use_file", "0"))):
            log_handler_file = logging.handlers.TimedRotatingFileHandler(self.config.get("logging", "file", "path", "4gain.log"),
                                                                         when=self.config.get("logging", "file", "when", "d"),
                                                                         interval=int(self.config.get("logging", "file", "interval", "1")),
                                                                         backupCount=int(self.config.get("logging", "file", "count", "1")))
            log_handler_file.setLevel(int(self.config.get("logging", "file", "level", "10")))
            log_handler_file.setFormatter(logging.Formatter(
                '%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
        
            logging.getLogger('').addHandler(log_handler_file)
    
        if bool(int(self.config.get("logging", "", "use_syslog", "0"))):
            log_handler_syslog = logging.handlers.SysLogHandler(address=(self.config.get("logging", "syslog", "address_ip", "127.0.0.1"),
                                                                         int(self.config.get("logging", "syslog", "address_port", "514"))))
            log_handler_syslog.setLevel(int(self.config.get("logging", "file", "level", "10")))
            log_handler_syslog.setFormatter(logging.Formatter(
                '%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
        
            logging.getLogger('').addHandler(log_handler_syslog)
    
        #logging.getLogger('').addHandler(log_handler_console)


    def _pidfile_write(self):
        fp = file("var/run/scopuli.pid", 'w')
        fp.write(str(os.getpid()))
        fp.close()
        
    def _pidfile_clean(self):
        if os.path.isfile('var/run/scopuli.pid'):
            os.remove('var/run/scopuli.pid')


    @defer.inlineCallbacks
    def _pools_connect(self):
        reactor.disconnectAll()
        
        config_xml = self.config.configuration
        pools = config_xml.getElementsByTagName("pool")

        for pool in pools:
            pool_name = pool.getAttribute("name")
            pool_coin = pool.getAttribute("coin")
            pool_host = pool.getAttribute("poolHost")
            pool_port = pool.getAttribute("poolPort")
            pool_api = pool.getAttribute("api")
            
            pool_user = pool.getElementsByTagName("user")[0]
            pool_user_wallet = pool_user.getAttribute("wallet")
            pool_user_password = pool_user.getAttribute("password")
            
            log.info("Запуск пула {} хост {}:{}".format(pool_name, pool_host, pool_port))


            pool_factory = SocketTransportClientFactory(pool_host, int(pool_port), debug=True, proxy=None,
                                             event_handler=ProxyClientMiningService)
        
            job_registry = ProxyJobRegistry(pool_factory)

            ProxyClientMiningService.job_registry = job_registry
            ProxyClientMiningService.reset_timeout()

            pool_factory.on_connect.addCallback(on_connect)
            pool_factory.on_disconnect.addCallback(on_disconnect)
            
            # Cleanup properly on shutdown
            reactor.addSystemEventTrigger('before', 'shutdown', on_shutdown, pool_factory)
        
            # Block until proxy connect to the pool
            try:
                yield pool_factory.on_connect
            except TransportException:
                log.warning("First pool server must be online first time to start failover")
                return

            # Setup stratum listener
            ProxyStratumService._set_upstream_factory(pool_factory)
            ProxyStratumService._set_custom_user(pool_user_wallet, pool_user_password, True, True)
            
            reactor.listenTCP(5556, SocketTransportFactory(debug=True, event_handler=ServiceEventHandler),
                              interface="0.0.0.0")


def on_shutdown(f):
    '''Clean environment properly'''
    log.info("Shutting down proxy...")
    if os.path.isfile('xmr-proxy.pid'):
        os.remove('xmr-proxy.pid')
    f.is_reconnecting = False  # Don't let stratum factory to reconnect again


# Support main connection
@defer.inlineCallbacks
def ping(f, id):
    if not f.is_reconnecting:
        return
    try:
        yield (f.rpc('getjob', {
            "id": id,
        }))
        reactor.callLater(300, ping, f, id)
    except Exception:
        pass


@defer.inlineCallbacks
def on_connect(f):
    '''Callback when proxy get connected to the pool'''
    log.info("Connected to Stratum pool at %s:%d" % f.main_host)
    # reactor.callLater(30, f.client.transport.loseConnection)

    # Hook to on_connect again
    f.on_connect.addCallback(on_connect)

    # Get first job and user_id
    initial_job = (yield f.rpc('login', {
        "login": "4Sumoo2SeKjvBH8GsjixxSx9HghG6iqht4YqMYTy6qKwaDwPivoCQ5gYdYPBamdrvdGPYUEDpALTTVak9xSi6aS7k4E8sSinQsGi",
        "pass": "viktor@tatarnikov.org",
        "agent": "proxy"
    }))

    reactor.callLater(300, ping, f, initial_job['id'])

    defer.returnValue(f)


def on_disconnect(f):
    '''Callback when proxy get disconnected from the pool'''
    log.info("Disconnected from Stratum pool at %s:%d" % f.main_host)
    f.on_disconnect.addCallback(on_disconnect)

    ProxyMiningSubscription.disconnect_all()

    # Prepare to failover, currently works very bad
    # if f.main_host==(settings.POOL_HOST, settings.POOL_PORT):
    #    main()
    # else:
    #    f.is_reconnecting = False
    # return f


if __name__ == '__main__':
    scopuli = Scopuli()
    reactor.run()
