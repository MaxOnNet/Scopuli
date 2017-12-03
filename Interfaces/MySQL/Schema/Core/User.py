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


class User(Base, Schema):
    """
        Таблица содержащая пользователей системы
    """
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица содержащая пользователей системы'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_group = Column(Integer(), ColumnDefault(1), nullable=False, doc="Ссылка на UserGroup")
    
    name_first = Column(String(64), nullable=False, doc="Имя")
    name_last = Column(String(64), nullable=False, doc="Фамилия")
    name_patronymic = Column(String(64), nullable=False, doc="Отчество")
    name_en = Column(String(64), nullable=False, doc="Имя в ASCII")
    
    is_delete = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")
    
    @hybrid_property
    def name_full(self):
        return " ".join([self.name_last, self.name_first, self.name_patronymic])


        # clubs = relationship("ClubUser", back_populates="user")


class UserGroup(Base, Schema):
    """
        Таблица групп пользователей
    """
    __tablename__ = 'user_group'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица групп пользователей'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_parent = Column(Integer(), ColumnDefault(1), ForeignKey(id), nullable=True, index=True, doc="Родитель")

    name = Column(String(64), nullable=False, doc="Имя группы")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Описание группы")
    order = Column(Integer(), ColumnDefault(1), nullable=False, doc="Порядковый номер в списках")
