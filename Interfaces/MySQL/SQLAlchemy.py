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

import uuid
import logging

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ColumnDefault, Float, text, Text, TypeDecorator, type_coerce, or_, desc
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import object_session, backref

from sqlalchemy_utils import URLType, CountryType, PhoneNumberType, UUIDType, IPAddressType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Schema:


    @staticmethod
    def translate(value):
        """
            Функция заглушка, выдает входящее значение без изменения, необходимо для SqlAlchemy.
    
            :param value: Значение
            :type value: String
            :return: ВХодящее значение без изменений
        """
        return value
