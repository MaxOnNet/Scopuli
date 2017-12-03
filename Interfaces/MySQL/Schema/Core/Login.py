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

from Interfaces.MySQL.Types import PasswordType

from Interfaces.MySQL.Schema import Base
from Interfaces.MySQL.Schema.Core.User import User
from Interfaces.MySQL.Schema.Core.Role import Role


class Login(Base, Schema):
    """
        Таблица логинов
    """
    __tablename__ = 'login'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица логинов'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_user = Column(Integer(), ForeignKey(User.id), index=True, nullable=False, doc="Ссылка на User")
    
    login = Column(String(64), nullable=False, doc="Логин")
    password = Column(String(64), nullable=False, doc="Пароль")
    password_hash = Column(PasswordType(), nullable=False, doc="Хэш пароля")
    
    date_start = Column(DateTime(), nullable=False, default=func.utc_timestamp())
    date_expire = Column(DateTime(), nullable=False)
    
    is_delete = Column(Boolean(), ColumnDefault(False), default=False, nullable=False, doc="Метка удаления")
    is_enable = Column(Boolean(), ColumnDefault(True), default=True, nullable=False, doc="Метка использования")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")
    
    _type_hash = {
        'inicialised': False
        }
    
    
    def _type_hash_init(self):
        if not bool(self._type_hash['inicialised']):
            query = """
                SELECT
                    lt.code as type_code,
                    lta.name as type_attribute,
                    COALESCE(ltav.value, lta.default) as type_attribute_value
                FROM
                    login_type as lt
                    JOIN login_param as lp on (lp.cd_login_type = lt.id and lp.is_enable = 1)
                    JOIN login_type_attribute as lta on (lta.cd_login_type = lt.id)
                    LEFT JOIN login_type_attribute_value as ltav  on (ltav.cd_login_param = lp.id and ltav.cd_login_type_attribute = lta.id)
                WHERE
                    lp.cd_login = {}
            """.format(self.id)
            
            for row in object_session(self).execute(text(query)):
                if row[0] not in self._type_hash:
                    self._type_hash[row[0]] = {}
            
            self._type_hash['inicialised'] = True
    
    
    def has_type(self, type_code):
        self._type_hash_init()
        
        return type_code in self._type_hash
    
    
    def get_type_attribute(self, type_code, type_attribute_name, default_value):
        self._type_hash_init()
        
        if type_code in self._type_hash:
            if type_attribute_name in self._type_hash[type_code]:
                return self._type_hash[type_code][type_attribute_name]
        
        return default_value


class LoginRole(Base, Schema):
    """
        Таблица связи логина и ролей
    """
    __tablename__ = 'login_role'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица связи логина и ролей'
        }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_login = Column(Integer(), ForeignKey('login.id'), index=True, nullable=False, doc="Ссылка на Login")
    cd_role = Column(Integer(), ForeignKey(Role.id), index=True, nullable=False, doc="Ссылка на Role")
    
    is_enable = Column(Boolean(), ColumnDefault(True), nullable=False, doc="Метка использования")


class LoginParam(Base, Schema):
    """
        Таблица с принадлежностями логина к типам
    """
    __tablename__ = 'login_param'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица с принадлежностями логина к типам'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_login = Column(Integer(), ForeignKey('login.id'), index=True, nullable=False, doc="Ссылка на Login")
    cd_login_type = Column(Integer(), ForeignKey('login_type.id'), index=True, nullable=False, doc="Ссылка на LoginType")
    
    is_enable = Column(Boolean(), ColumnDefault(True), nullable=False, doc="Метка использования")


class LoginType(Base, Schema):
    """
        Таблица возможных типов логина
    """
    __tablename__ = 'login_type'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица возможных типов логина'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    code = Column(String(64), unique=True, index=True, nullable=False, doc="Кодовое обозначение типа")
    name = Column(String(256), nullable=False, doc="Наименование типа")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Дополнительная информация по типу")


class LoginTypeAttribute(Base, Schema):
    """
        Таблица возможных атрибутов логина
    """
    __tablename__ = 'login_type_attribute'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица возможных атрибутов логина'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_login_type = Column(Integer(), ForeignKey('login_type.id'), index=True, nullable=False, doc="Ссылка на LoginType")
    
    name = Column(String(256), nullable=False, doc="Наименование атрибута")
    description = Column(String(256), ColumnDefault(""), nullable=False, doc="Дополнительная информация по типу")
    default = Column(String(256), ColumnDefault(""), nullable=False,
                     doc="Дефолтное значение, принимается если logins_attribute_value пуста")
    type = Column(String(64), ColumnDefault("STR"), nullable=False, doc="Тип данных")


class LoginTypeAttributeValues(Base, Schema):
    """
        Таблица значений атрибутов логина
    """
    __tablename__ = 'login_type_attribute_value'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci',
        'mysql_comment': 'Таблица значений атрибутов логина'
    }
    
    id = Column(Integer(), primary_key=True, autoincrement=True, doc="Row ID - Сурогатный ключ")
    cd_login_param = Column(Integer(), ForeignKey('login_param.id'), index=True, nullable=False, doc="Ссылка на LoginParam")
    cd_login_type_attribute = Column(Integer(), ForeignKey('login_type_attribute.id'), index=True, nullable=False,
                                     doc="Ссылка на LoginTypeAttribute")
    
    value = Column(String(256), ColumnDefault(""), nullable=False, doc="Значение атрибута")
    
    # Automatic Logger
    date_create = Column(DateTime(), nullable=False, default=func.utc_timestamp(), doc="AutoLogger - Время создания")
    date_change = Column(DateTime(), nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp(),
                         doc="AutoLogger - Время последнего изменения")

