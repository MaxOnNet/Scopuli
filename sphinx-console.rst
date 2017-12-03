.. _application_console:

Консольные приложения
=====================

Проект содержит множество консольных утилит как для непосредственной работы, так и для облегчения разработки.

.. only:: html
    .. contents:: Сoдержание документа
        :depth: 2
        :local:

База данных
-----------

.. _application_db_backup:

4gain-db-backup.sh
~~~~~~~~~~~~~~~~~~
Место запуска: ``Any``. Скрипт: :download:`4gain-db-backup.sh <./4gain-db-backup.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-db-backup.sh;



.. _application_db_restore:

4gain-db-restore.sh
~~~~~~~~~~~~~~~~~~~
Место запуска: ``Any``. Скрипт: :download:`4gain-db-restore.sh <./4gain-db-restore.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-db-restore.sh;



Установка
---------

.. _application_install_devel:

4gain-install-devel.sh
~~~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-install-devel.sh <./4gain-install-devel.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-install-devel.sh;



.. _application_install_gui:

4gain-install-gui.sh
~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Manager Station``. Скрипт: :download:`4gain-install-gui.sh <./4gain-install-gui.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-install-gui.sh;



.. _application_install_web:

4gain-install-web.sh
~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Web Application Server``. Скрипт: :download:`4gain-install-web.sh <./4gain-install-web.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-install-web.sh;



.. _application_requirements_update:

4gain-requirements-update.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-requirements-update.sh <./4gain-requirements-update.sh>`.

Скрипт обновления ``requirements.txt`` исходя из установленных компонентов окружения.

.. code-block:: bash

    # Запуск
    ./4gain-requirements-update.sh;



Запуск
------

.. _application-run_gui:

4gain-run-gui.sh
~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station`` | ``Manager Station``. Скрипт: :download:`4gain-run-gui.sh <./4gain-run-gui.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-run-gui.sh;



.. _application_run_gui:

4gain-run-web.sh
~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-run-web.sh <./4gain-run-web.sh>`.

.. code-block:: bash

    # Запуск
    ./4gain-stable-web.sh;


Web Сервер
----------

Утилиты создания окружения для Apache, сборки документации Sphinx.

.. _application_server:

4gain-server.py
~~~~~~~~~~~~~~~
Место запуска: ``Web Application Server``. Скрипт: :download:`4gain-server.py <./4gain-server.py>`.

.. code-block:: bash

    # Запуск
    ./4gain-server-web.py;



.. _application_sphinx_update:

4gain-sphinx-update.sh
~~~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-sphinx-update.sh <./4gain-sphinx-update.sh>`.

Скрипт сборщик автодокументации Sphinx и построения графиков зависимостей SQL.

.. code-block:: bash

    # Запуск
    ./4gain-sphinx-update.sh;



.. _application_md_update:

4gain-md-update.py
~~~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-md-update.py <./4gain-md-update.py>`.

.. code-block:: bash

    # Запуск
    ./4gain-md-update.py;



Утилиты развертывания
---------------------
Утилиты отделения "мух от котлет". На рабочей системе нет необходимости хранить весь набор данных проекта. Данные утилиты позволяют подготовить обособленное окружение очищенное от лишних файлов.

Также данные скрипты применяются для разделения ветки разработчика от продакшена.

.. _application_stable_gui:

4gain-stable-gui.sh
~~~~~~~~~~~~~~~~~~~
Место запуска: ``Web Application Server``. Скрипт: :download:`4gain-stable-gui.sh <./4gain-stable-gui.sh>`.

Утилита разделения кодовой базы, выделяет из общего дерева проекта ``/home/engine`` файлы необходимы для работы GUI приложения и переносит их в ``/home/engine.gui`` для дальнейшего деплоя на рабочие станции.

.. code-block:: bash

    # Запуск
    ./4gain-stable-gui.sh;



.. _application_stable_web:

4gain-stable-web.sh
~~~~~~~~~~~~~~~~~~~
Место запуска: ``Web Application Server``. Скрипт: :download:`4gain-stable-web.sh <./4gain-stable-web.sh>`.

Утилита разделения кодовой базы, выделяет из общего дерева проекта ``/home/engine`` файлы необходимы для работы Web приложений и переносит их в ``/home/engine.web``.

Перенос происходит по следующей схеме:

#. Остановка Web сервера.
#. Размонтирование всех виртуальных каталогов Web приложений.
#. Перенос файлов.
#. Монтирование виртуальных каталогов Web приложений.
#. Запуск Web сервера.

.. code-block:: bash

    # Запуск
    ./4gain-stable-web.sh;



.. _application_stable_web_host:

4gain-stable-web-vhost.sh
~~~~~~~~~~~~~~~~~~~~~~~~~
Место запуска: ``Devel Station``. Скрипт: :download:`4gain-stable-web-vhost.sh <./4gain-stable-web-vhost.sh>`.

Утилита переноса данных разработки web приложения в продакшен.

.. code-block:: bash

    # Example:
    #   ./4gain-stable-web-host.sh pro-4gain-ambclub ru-ambclub

    # Запуск
    ./4gain-stable-web-host.sh <vhost_src_name> <vhost_dst_name>;

