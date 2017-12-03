forGain Engine Documentation
============================

.. sidebar:: Коротко о документе

    Данный проект на стадии сверх активного развития и передокументирования, поэтому информация обновляется / дополняется каждый день.

    .. |date| date::
    .. |time| date:: %H:%M

    Этот документ был сгенерирован |date| в |time|.

Данный проект изначально задумывался как панель управления Фитнесс клубом, абонементы, учет поминутных услуг и ведение бара.
Но не успела завершиться подготовка первого альфа релиза, как проект перерос в нечто большее, и продолжает обрастать различными фишками.

Структура проекта
-----------------
Проект делится на несколько основных частей.

#. DataBase
#. GUI Application
#. Web Application
#. Console Application's

Структура кодовой базы
----------------------
.. toctree::
    :maxdepth: 10
    :titlesonly:

    Interfaces/__module
    GUI/__module
    WEB/__module
    Server/__module

Дополнения и разный хлам
------------------------
.. toctree::
    :maxdepth: 3
    :titlesonly:

    SQL/__module
    share/__module


Документация и утилиты
----------------------
.. toctree::
    :maxdepth: 2

    sphinx-console
    sphinx-config
    sphinx-todolist

Примеры использования кодовой базы
----------------------------------
#. `4gain.pro <http://4gain.pro/>`_ - Основная сайт визитка
#. `engine.4gain.pro <http://engine.4gain.pro/>`_ - Описание возможностей кодовой базы, примеры
#. `ambclub.ru <http://ambclub.ru/>`_ - Сайт ЦСД Амбассадор. В нем используется наибольшее количество функций :abbr:`4GE (4Gain Engine)`. Помимо :abbr:`4GW (4Gain Web)`, в клубе используется :abbr:`4GG (4Gain GUI)` под Fedora Linux.
#. `betar-siberia.ru <http://betar-siberia.ru/>`_ - Сайт ПФК Бетар-Сибирь. Легкий портал, со статьями, каталогом и контактами.
#. `uchetenergo.com <http://uchetenergo.com/>`_ - Сайт сети магазинов "Счетсчики".

Поиск и индексы
---------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
