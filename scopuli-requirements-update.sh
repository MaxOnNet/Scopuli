#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright [2016] Tatarnikov Viktor [viktor@tatarnikov.org]
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

# Проверяем наличия переменной с адресом графического интерфейса
if [ -z "${DISPLAY}" ]; then
    export DISPLAY=:0.0
fi;

# Проверяем, присутствует ли отладочное окружение
path_python_env="/Users/v_tatarnikov/ownCloud/Projects/_pycharm/_env/_4gain";

if [ -x "${path_python_env}/bin/python" ]; then
    echo "USE Python path: ${path_python_env}";
    path_pip="${path_python_env}/bin/pip";
    path_python="${path_python_env}/bin/python";
else
    path_pip="$(which pip)";
    path_python="$(which python)";
fi;

# Ищем путь до программы
for path in  "/Users/v_tatarnikov/ownCloud/Projects/_pycharm/Scopuli/" "/home/scopuli/"; do
    if [ -e "${path}scopuli-requirements-update.sh" ]; then
        echo "USE Scopuli path: ${path}";


        ${path_pip} freeze > ${path}/requirements.txt;
        break;
    fi;
done;
