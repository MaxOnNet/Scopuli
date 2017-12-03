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

import logging

#   Twisted
from twisted.internet import reactor

#   Stratum
from Interfaces.Stratum.event_handler import GenericEventHandler

#   Proxy
from Interfaces.Proxy.Job import ProxyJob
from Interfaces.Proxy.StratumService import ProxyMiningSubscription


log = logging.getLogger(__name__)


class ProxyClientMiningService(GenericEventHandler):
    job_registry = None     # Reference to JobRegistry instance
    timeout = None          # Reference to IReactorTime object
    
    @classmethod
    def reset_timeout(cls):
        if cls.timeout != None:
            if not cls.timeout.called:
                cls.timeout.cancel()
            cls.timeout = None
            
        cls.timeout = reactor.callLater(960, cls.on_timeout)

    @classmethod
    def on_timeout(cls):
        """
            Try to reconnect to the pool after 16 minutes of no activity on the connection.
            It will also drop all Stratum connections to sub-miners
            to indicate connection issues.
        """
        log.error("Connection to upstream pool timed out")
        cls.reset_timeout()
        cls.job_registry.f.reconnect()
                
    def handle_event(self, method, params, connection_ref):
        """Handle RPC calls and notifications from the pool"""
        
        # Yay, we received something from the pool,
        # let's restart the timeout.
        self.reset_timeout()
        
        if method == 'job':
            """Proxy just received information about new mining job"""
            
            if 'id' not in params:
                (blob, job_id, target, user_id) = params["blob"], params["job_id"], params["target"], 1
            else:
                (blob, job_id, target, user_id) = params["blob"], params["job_id"], params["target"], params["id"]
        
            # Broadcast to Stratum client
            ProxyMiningSubscription.on_template(job_id, blob, target, user_id)
            
            # Broadcast to getwork clients
            job = ProxyJob.build_from_pool(job_id, blob, target)
            log.info("New job %s for %s" % (job_id, user_id))

            self.job_registry.add_job(job, True)
            
        else:
            """Pool just asked us for something which we don't support..."""
            log.error("Unhandled method %s with params %s" % (method, params))

