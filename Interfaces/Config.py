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
""" """


from functools import wraps
import xml.dom.minidom
import os


class Config:
    """
        Класс отвечаюший за работу с конфигурационными файлами.

        Пример конфигурационного файла:
        
        .. code-block:: xml
            :linenos:
            
            <?xml version="1.0" encoding="UTF-8"?>
            <configuration>
                <group_name group_attr_one="0" group_attr_two="GroupAttrValue">
                    <section_name_one section_attr_one="SectionAttrValue"/>
                    <section_name_two section_attr_two="SectionAttrValue" section_attr_one="3" />
                </group_name>
            </configuration>
            
        Пример использования:
        
        .. code-block:: python
            :linenos:
            
            config = Config()
            config.set("database", "mysql", "server", "10.19.2.21")     // save value
            config.set("database", "mysql", "username", "root")         // save value
            config.get("database", "mysql", "server", "127.0.0.1")      // get value, return 10.19.2.21
            config.remove("database", "mysql", "username")
            config.save()
        
    """

    def __init__(self):
        """
            Инициализация класса, загружает **две** версии конфигурационного файла:
    
            #. **app-root/config.xml** - используется как основной.
            #. **web-root/.4gain.etc/config.xml** - используется для переопределения значений из первого конфига.
            
            Если существует второй конфигурационный фаил, то все изменения записываются в него.
            
            :return: None, функция ничего не возвращает.
            :rtype: Nothing
        """
        self.xml_file_web = "{0}/config.xml".format(os.path.abspath(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), '../../.4gain.etc')))
        
        self.xml_file = "{0}/config.xml".format(os.path.abspath(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), '..')))
        
        self.xml = xml.dom.minidom.parse(self.xml_file)
        self.configuration = self.xml.getElementsByTagName("configuration")[0]

        if os.path.isfile(self.xml_file_web):
            self.xml_web = xml.dom.minidom.parse(self.xml_file_web)
            self.configuration_web = self.xml_web.getElementsByTagName("configuration")[0]
        else:
            self.xml_web = None
            self.configuration_web = None
     
            
    def fix_parms(fn):
        """
            Декоратор.
            
            Используется для переопределения возвращаемого значения из **get** функции. И переопределяем следующие ключевые слова:
            
            #. **$path** - Изменяет на путь до основного каталога проекта, где и лежит **config.xml**.
            #. **$apache** - Изменяет на путь до основного каталога на веб сервере.
            
            :return: Измененное значение функции.
            :rtype: String
        """
        @wraps(fn)
        def wrapped(*args, **kwargs):
            value_o = str(fn(*args, **kwargs))
            value_n = value_o

            value_n = str.replace(value_n, "$path", str(os.path.abspath(os.path.join(os.path.dirname(
                os.path.realpath(__file__)), '..'))))

            value_n = str.replace(value_n, "$apache", str(os.path.abspath(os.path.dirname(os.path.realpath(os.getcwd())))))

            return value_n
        return wrapped


    @fix_parms
    def get(self, group, item, attribute, value=""):
        """
            Функция получения значения из конфигурационного файла.
            Если существует web-root/.4gain.etc/config.xml, то поиск изначально идет в нем, далее переходим на основной конфигурационный фаил.
            
            :param group: Имя группы в конфигурационном файле.
            :type group: String
            :param item: Имя секции в конфигурационном файле. Если имя секции опущено, идет поиск атрибута у группы.
            :type item: String
            :param attribute: Имя аттрибута секции в конфигурационном файле
            :type attribute: String
            :param value: Дефолтное значение, испоьзуется если не найдено искомое, по умолчанию "".
            :type value: String
            
            :return: Искомое значение или дефолтное значение.
            :rtype: String
        """

        # Todo: Добавить возможность переопределать изменяемый конфигурационный фаил

        if self.xml_web:
            for _group in self.configuration_web.getElementsByTagName(group):
                if item == "":
                    if _group.hasAttribute(attribute):
                        return _group.getAttribute(attribute)
                else:
                    for _item in _group.getElementsByTagName(item):
                        if _item.hasAttribute(attribute):
                            return _item.getAttribute(attribute)
        
        for _group in self.configuration.getElementsByTagName(group):
            if item == "":
                if _group.hasAttribute(attribute):
                    return _group.getAttribute(attribute)
            else:
                for _item in _group.getElementsByTagName(item):
                    if _item.hasAttribute(attribute):
                        return _item.getAttribute(attribute)
                    
        return value


    def set(self, group, item, attribute, value=""):
        """
            Функция записи значения в конфигурационного файла.
            Если существует web-root/.4gain.etc/config.xml, то запись идет в него, основной фаил игнорируется.
            
            :param group: Имя группы в конфигурационном файле.
            :type group: String
            :param item: Имя секции в конфигурационном файле. Если имя секции опущено, идет поиск атрибута у группы.
            :type item: String
            :param attribute: Имя аттрибута секции в конфигурационном файле
            :type attribute: String
            :param value: Значение параметра для записи, по умолчанию "".
            :type value: String
            :return: None, функция ничего не возвращает.
            :rtype: Nothing
        """

        # Todo: Добавить возможность переопределать изменяемый конфигурационный фаил
        
        configuration = self.configuration
        xml = self.xml
        
        if self.xml_web:
            configuration = self.configuration_web
            xml = self.xml_web
            
        if len(configuration.getElementsByTagName(group)) == 0:
            configuration.appendChild(xml.createElement(group))

        for _group in configuration.getElementsByTagName(group):
            if item == "":
                _group.setAttribute(attribute, value)
            else:
                if len(_group.getElementsByTagName(item)) == 0:
                    _group.appendChild(xml.createElement(item))

                for _item in _group.getElementsByTagName(item):
                    _item.setAttribute(attribute, value)

        self.save()


    def remove(self, group, item, attribute):
        """
            Функция удаления значения в конфигурационного файла.
            Если существует web-root/.4gain.etc/config.xml, то запись идет в него, основной фаил игнорируется.
            И удалить что либо из основного конфига не возможно.
            
            :param group: Имя группы в конфигурационном файле.
            :param item: Имя секции в конфигурационном файле. Если имя секции опущено, идет поиск атрибута у группы.
            :param attribute: Имя аттрибута секции в конфигурационном файле
            :return: None, функция ничего не возвращает.
            :rtype: Nothing
        """

        # Todo: Добавить возможность переопределать изменяемый конфигурационный фаил

        configuration = self.configuration
    
        if self.xml_web:
            configuration = self.configuration_web
    
        for _group in configuration.getElementsByTagName(group):
            if item == "" and attribute != "":
                if _group.hasAttribute(attribute):
                    _group.removeAttribute(attribute)

            elif item == "" and attribute == "":
                configuration.removeChild(_group)

            else:
                for _item in _group.getElementsByTagName(item):
                    if attribute != "":
                        if _item.hasAttribute(attribute):
                            _item.removeAttribute(attribute)
                    else:
                        _group.removeChild(_item)

        self.save()


    def save(self):
        """
            Функция записи конфигурационного файла на диск.
            Сохраняются оба конфигурационных файла.
            
            :return: None, функция ничего не возвращает.
            :rtype: Nothing
        """
        io_writer = open(self.xml_file, "w")
        io_writer.writelines(self.xml.toprettyxml(indent="", newl="", encoding="UTF-8"))
        io_writer.close()

        if self.xml_web:
            io_writer = open(self.xml_file_web, "w")
            io_writer.writelines(self.xml_web.toprettyxml(indent="", newl="", encoding="UTF-8"))
            io_writer.close()
