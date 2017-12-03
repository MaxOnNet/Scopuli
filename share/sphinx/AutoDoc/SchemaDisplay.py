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
import logging

from Interfaces.Config import Config
from Interfaces.MySQL import Schema

log = logging.getLogger(__name__)


class SchemaDisplay:
    """
        Класс визуализации модели базы данных на основе ORM SQLAlchemy.
        
        Для работы необходимы: ``pydot``, ``graphviz``.
        
        Параметры конфигурационного файла:
        
        .. code-block:: xml
            :linenos:
            
            <?xml version="1.0" encoding="UTF-8"?>
            <configuration>
                <sphinx>
                    <AutoDocSchemaDisplay path_graph="$path/share/sphinx/static/schema_graph.png" />
                </sphinx>
            </configuration>
    
    """
    def __init__(self):
        self.config = Config()
        
        self.path_graph = self.config.get("sphinx", "AutoDocSchemaDisplay", "path_graph", "")

        # Инициализация параметров логирования.
        logging.basicConfig(level=int(self.config.get("logging", "console", "level", "10")), stream=sys.stdout,
                            format='%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s')


    def render_schema(self):
        """
            Отрисовка структуры схемы БД.
            Записывает построенный график в фаил.
            
            :return: None
        """
        from sqlalchemy_schemadisplay import create_uml_graph, create_schema_graph
        from sqlalchemy.orm import class_mapper
    
        log.info("Формирование списка таблиц.")

        mappers = []
        for schema_name in dir(Schema):
            if schema_name[0] == '_':
                continue
                
            if schema_name in ['Base', 'log']:
                continue

            schema_class = getattr(Schema, schema_name)
            
            if hasattr(schema_class, "__tablename__"):
                log.debug("    Анализ схемы: {}".format(schema_name))
                
                mappers.append(class_mapper(schema_class))
       
        log.info("Формирование окружения GraphViz.")
        
        graph = create_uml_graph(
            mappers,
            show_inherited=False,
            show_operations=False,
            show_datatypes=False,
            show_multiplicity_one=False
        )

        log.info("Формирование графика.")
        graph.write_png(self.path_graph)

        log.info("Формирование графика завершено.")

if __name__ == "__main__":

    adsd = SchemaDisplay()
    adsd.render_schema()
