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

export PATH=$PATH:/usr/local/bin;

# Проверяем, присутствует ли отладочное окружение
path_python_env="/Users/v_tatarnikov/ownCloud/Projects/_pycharm/_env/_4gain";

if [ -x "${path_python_env}/bin/python" ]; then
    echo "USE Python path: ${path_python_env}";
    path_python="${path_python_env}/bin/python";
else
    path_python="$(which python)";
    path_python_env="/";
fi;

sphinx_output_type="$1";

if [ -z "${sphinx_output_type}" ]; then
    sphinx_output_type="pd";
fi;

# Ищем путь до программы
for path in  "/Users/v_tatarnikov/ownCloud/Projects/_pycharm/Scopuli/" "/home/scopuli/"; do
    if [ -e "${path}scopuli-sphinx-update.sh" ]; then
        echo "USE Scopuli path: ${path}";
        cd ${path}/;

        if [ "${sphinx_output_type}" == "html" ]; then
            PYTHONUNBUFFERED=1 LC_CTYPE=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LC_COLLATE=ru_RU.utf8 LC_MONETARY=ru_RU.utf8 PYTHONPATH=${PYTHONPATH}:${path} ${path_python_env}/bin/sphinx-build -b ${sphinx_output_type} -E -d ./share/sphinx/build/doctrees/ -j 1 -c ./share/sphinx/ ./ ./share/sphinx/build/html;

            break;
        fi;

        if [ "${sphinx_output_type}" == "latex" ]; then
            export PATH=$PATH:/usr/local/texlive/2016/bin/x86_64-darwin/;
            PYTHONUNBUFFERED=1 LC_CTYPE=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LC_COLLATE=ru_RU.utf8 LC_MONETARY=ru_RU.utf8 PYTHONPATH=${PYTHONPATH}:${path} ${path_python_env}/bin/sphinx-build -b ${sphinx_output_type} -E -d ./share/sphinx/build/doctrees/ -j 1 -c ./share/sphinx/ ./ ./share/sphinx/build/latex ;

            cd ${path}/share/sphinx/build/latex;
            echo "Запускаем LaTeX в PDF конвертер."
            make > /dev/null 2> /dev/null;
            echo "Копируем полученный PDF в 'sphinx/static'."
            cp ${path}/share/sphinx/build/latex/Scopuli.pdf ${path}/share/sphinx/static/Scopuli.pdf;
            echo "Очищаем временные файлы конвертера.";
            make clean > /dev/null 2> /dev/null;
            break;
        fi;

        echo "Sphinx output is ${sphinx_output_type} and not is html or latex";
        break;
    fi;
done;


