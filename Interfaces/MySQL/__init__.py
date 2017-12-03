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


from Interfaces.MySQL.SQLAlchemy import create_engine, scoped_session, sessionmaker
from Interfaces.MySQL.Schema import Base


def init(config):
    mysql_engine = create_engine('mysql+pymysql://{0}:{1}@{2}'.format(
        config.get("database", "mysql", "user"),
        config.get("database", "mysql", "password"),
        config.get("database", "mysql", "server")
    ))

    mysql_engine.execute("CREATE DATABASE IF NOT EXISTS {0} "
                         "DEFAULT CHARACTER SET = '{1}' DEFAULT COLLATE 'utf8_unicode_ci'".format(
        config.get("database", "mysql", "database"),
        config.get("database", "mysql", "charset", "utf8")
    ))

    mysql_engine.dispose()
    
    return init_fast(config)


def init_fast(config):
    # Go ahead and use this engine
    db_engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}?charset={4}'.format(
        config.get("database", "mysql", "user"),
        config.get("database", "mysql", "password"),
        config.get("database", "mysql", "server"),
        config.get("database", "mysql", "database"),
        config.get("database", "mysql", "charset", "utf8"),
        
    ), isolation_level="READ COMMITTED", strategy='threadlocal')

    Base.metadata.create_all(db_engine)

    return scoped_session(
        sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=db_engine.execution_options(isolation_level='READ COMMITTED')
            )
        )
