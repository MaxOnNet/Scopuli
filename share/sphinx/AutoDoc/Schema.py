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
reload(sys)

sys.setdefaultencoding('utf8')

from collections import OrderedDict


class Schema:
    """
        Класс хелпер, анализирует содержимое класса, если это описание таблицы ORM SqlAlchemy, то скрывает из Sphinx'a AutoDoc'a столбцы и связи, а потом выводит их в удобной таблице в шапке класса.
        А также выводит SQL код создания таблицы.
        
        .. todo: Добавить графическую отрисовку связей таблиц.
        
    """
    def __init__(self, object):
        self.object = object

        self._table_name = "undef"
        self._table_args = {}
        self._table_engine = "undef"
        self._table_description = "undef"
        self._table_charset = "undef"
        self._table_collate = "undef"
        self._table_module = ""
        self._table_class = ""
        
        self._table_columns = {}
        self._table_links = {}
        

    def rst_name(self, name):
        """
            Функция переименования названия модуля под ссылку в rst
            
            :param name: Имя модуля или класса
            :type name: String
            :return: Имя ссылки в rst
            :rtype: String
        """
        return name.lower().replace(".", "-")


    def has_schema(self):
        """
            Функция определения, является ли обьект схемой ORM SqlAlchemy.
            
            :return: True если это класс схемы ORM SqlAlchemy, иначе False
            :rtype: Boolean
        """
        attrs = ["__tablename__", "__table_args__"]
        
        for attr in attrs:
            if not hasattr(self.object, attr):
                return False
            
        return True

    def has_schema_attr(self):
        """
            Функция определения, является ли обьект атрибутом класса ORM SqlAlchemy.
    
            :return: True если это атрибут схемы ORM SqlAlchemy, иначе False
            :rtype: Boolean
        """
        if hasattr(self.object, 'prop'):
            if hasattr(self.object.prop, 'strategy_wildcard_key'):
                if self.object.prop.strategy_wildcard_key in ['column', 'relationship']:
                    return True
            
        return False


    def get_attr_order(self, key):
        """
            Функция определения порядкового номера в сортировке столбцов таблицы по имени столбца.
    
            :param key: Название столбца
            :type key: String
            :return: Порядковый номер сортировки
            :rtype: Integer
        """
        key_prefix = key.split("_")[0]
    
        if key_prefix in ['id']:
            return 0
        elif key_prefix in ['cd']:
            return 1
        elif key_prefix in ['is']:
            return 2
        elif key_prefix in ['web']:
            return 4
        elif key_prefix in ['date']:
            return 5
        else:
            return 3


    def parse_table(self):
        """
            Функция анализа класса и получения данных о схеме.
            
            :return: None
            :rtype: Nothing
        """
        self._table_name = getattr(self.object, "__tablename__", self._table_name)
        self._table_args = getattr(self.object, "__table_args__", self._table_args)
        self._table_module = getattr(self.object, "__module__", self._table_module)
        self._table_class = getattr(self.object, "__name__", self._table_class)
        
        if "mysql_engine" in self._table_args:
            self._table_engine = self._table_args['mysql_engine']
            
        if "mysql_charset" in self._table_args:
            self._table_charset = self._table_args['mysql_charset']
            
        if "mysql_collate" in self._table_args:
            self._table_collate = self._table_args['mysql_collate']
            
        if "mysql_comment" in self._table_args:
            self._table_description = self._table_args['mysql_comment']


    def parse_columns(self):
        """
            Функция анализа класса и получения данных о схеме.
    
            :return: None
            :rtype: Nothing
        """
        for attr_key in self.object.__dict__.keys():
            if attr_key in self.object._sa_class_manager:
                
                if self.object._sa_class_manager[attr_key].prop.strategy_wildcard_key == 'column':
                    self._table_columns[attr_key] = {}
                    self._table_columns[attr_key]['order'] = self.get_attr_order(attr_key)
                    self._table_columns[attr_key]['name'] = attr_key
                    self._table_columns[attr_key]['description'] = str(self.object._sa_class_manager[attr_key].prop.doc).replace(",", "")
                    self._table_columns[attr_key]['type'] = str(self.object._sa_class_manager[attr_key].prop.columns[0].type).lower()

                if self.object._sa_class_manager[attr_key].prop.strategy_wildcard_key == 'relationship':
                    # Мои зависимости сугубо с маленькой буквы
                    if 97 <= ord(attr_key[0]) <= 122:
                        self._table_links[attr_key] = {}
                        self._table_links[attr_key]['name'] = attr_key
                        self._table_links[attr_key]['description'] = str(self.object._sa_class_manager[attr_key].prop.doc).replace(",", "")
                        self._table_links[attr_key]['type'] = "relationship"
                        self._table_links[attr_key]['table'] = self.object._sa_class_manager[attr_key].prop.mapper.entity.__name__
                        self._table_links[attr_key]['module'] = self.object._sa_class_manager[attr_key].prop.mapper.entity.__module__

            
    def render(self, lines):
        """
            Функция отрисовки данных в rst. Функция ничего не возвращает, а заменяет данные в массиве.
            
            :param lines: Массив строк с описанием класса от AutoDoc'a Sphinx'a
            :type lines: Array of string
            :return: None
            :rtype: Nothing
        """
        if self.has_schema():
            lines_original = []
            
            # Зануляем содержиное
            for line_index in xrange(len(lines)):
                lines_original.append(str(lines[line_index]))
                lines[line_index] = ""
                
            #
            #   Отрисовка шапки
            #
            lines.append(u"""Класс '``{tclass}``' определяет структуру SQL таблицы '``{tname}``' [Engine: {tengine}; Charset: {tcharset}; Collate: {tcollate}]. """.format(tclass=self._table_class, tname=self._table_name, tengine=self._table_engine, tcharset=self._table_charset, tcollate=self._table_collate))
            lines.append(u"""""")
            
            lines.append(u"""Класс содержит: столбцов ``{}``; подключенных связей ``{}``.""".format(len(self._table_columns), len(self._table_links)))
            lines.append(u"""""")
            
            #
            #   Отрисовка таблицы
            #
            lines.append(u""".. rubric:: Логическое описание полей таблицы.""")
            lines.append(u"""""")

            lines.append(u""".. _schema-{}-{}:""".format(self.rst_name(self._table_module), self.rst_name(self._table_class)))
            lines.append(u""".. cssclass:: table-striped""")
            
            lines.append(u""".. csv-table:: SQL Table: {} ({})""".format(self._table_class, self._table_description))
            lines.append(u"""    :header: Название, Тип, Описание""")
            lines.append(u"""    :widths: 10, 10, 50""")
            lines.append(u"""    :stub-columns: 1""")
            lines.append(u"""""")
            
            columns_keys = OrderedDict(sorted(self._table_columns.items(), key=lambda t: (t[1]['order'], t[0])))
            
            for column_key in columns_keys:
                column = self._table_columns[column_key]
                
                if column['description'] == "":
                    column['description'] = " "
                lines.append(u"""    {}, {}, {}""".format(column['name'], column['type'], column['description']))
            
            links_keys = OrderedDict(sorted(self._table_links.items(), key=lambda t: (t[1]['name'], t[0])))
            
            for link_key in links_keys:
                link = self._table_links[link_key]
                    
                lines.append(u"""    {}, {}, :ref:`schema-{}-{}`""".format(link['name'], link['type'], self.rst_name(link['module']), self.rst_name(link['table'])))

            lines.append(u"""""")
            
            #
            #   Генерация SQL
            #
            from sqlalchemy.schema import CreateTable
    
            sql_raw = str(CreateTable(self.object.__table__))
            lines.append(u""".. rubric:: Vanila SQL: Создание таблицы ``{}``.""".format(self._table_name))
            lines.append(u"""""")
            lines.append(u""".. code-block:: sql """)
            lines.append(u"""    :linenos:""")
    
            for line in sql_raw.splitlines():
                lines.append(u"""    {}""".format(line))
    
            lines.append(u"""""")
            
            #
            #   Описание из автодокументации
            #
            lines.append(u""".. rubric:: Описание класса ``{}``.""".format(self._table_class))
            lines.append(u"""""")
            for line_index in xrange(len(lines_original)):
                lines.append(lines_original[line_index])

            lines.append(u"""""")
            
            #
            #   Добавление рубрики
            #
            lines.append(u""".. rubric:: Бизнес логика схемы ``{}``.""".format(self._table_class))
            lines.append(u"""""")


if __name__ == "__main__":
    from Interfaces.MySQL import Schema as sqlSchemna
    lines = []

    schema = Schema(object=sqlSchemna.WebSite)

    if schema.has_schema():
        print "Object is Schema."
        schema.parse_table()
        schema.parse_columns()
        schema.render(lines=lines)

        print ":    reStructuredText Start"
        print u"\n".join(lines)
        print ":    reStructuredText End"
        
    elif schema.has_schema_attr():
        print "Object is Schema Attribute."
        
    else:
        print "Object is not Schema element."

