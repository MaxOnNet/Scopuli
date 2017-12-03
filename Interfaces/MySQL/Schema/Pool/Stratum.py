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

from Interfaces.MySQL.SQLAlchemy import *

from Interfaces.MySQL.Schema import Base, log
from Interfaces.MySQL.Schema.Pool import Pool


class PoolStratum(Base, Schema):
    """
    
    """
    __tablename__ = 'pool_stratum'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': ''
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_pool = Column(Integer(), ForeignKey(Pool.id), index=True, nullable=False, doc="Ссылка на Pool")
    
    port = Column(Integer(), ColumnDefault(1), nullable=False, doc="")
    difficulty = Column(Integer(), ColumnDefault(1), nullable=False, doc="")
    
    is_enable = Column(Boolean(), ColumnDefault(True), nullable=False, doc="Метка использования")
    
    # Automatic Logger
    date_lastactive = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="Время последнего обращения")
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")

