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


log = logging.getLogger(__name__)


class ProxyJob(object):
    def __init__(self):
        self.job_id = ''
        self.blob = ''
        self.target = ''

    @classmethod
    def build_from_pool(cls, job_id, blob, target):
        """Build job object from Stratum server broadcast"""
        job = ProxyJob()
        job.job_id = job_id
        job.blob = blob
        job.target = target
        return job


