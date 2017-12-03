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
from twisted.internet import defer


log = logging.getLogger(__name__)


class ProxyJobRegistry(object):
    def __init__(self, f):
        self.f = f
        self.jobs = []
        # Hook for LP broadcasts
        self.on_block = defer.Deferred()
    
    
    def add_job(self, template, clean_jobs):  # ????clean
        if clean_jobs:
            # Pool asked us to stop submitting shares from previous jobs
            self.jobs = []
        
        self.jobs.append(template)
        
        if clean_jobs:
            # Force miners to reload jobs
            on_block = self.on_block
            self.on_block = defer.Deferred()
            on_block.callback(True)
