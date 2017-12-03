.. _example-config:

Конфигурационные файлы
======================

Конфигурационные файлы хранятся вот в такой файловой структуре:


.. code-block:: bash
    :linenos:

    /home/engine/config.xml # (4GE Сonfig)
    /home/apache/pro-4gain/.4gain.etc/config.xml # (4GW Сonfig для 4gain.pro)
    /home/apache/pro-4gain-engine/.4gain.etc/config.xml # (4GW Сonfig для engine.4gain.pro)


.. _example-config-4ge:

Конфигурационный фаил 4GE
-------------------------

Пример "классического" конфигурационного файла:

.. code-block:: xml
    :linenos:

    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <database use_synchronizer="0" use_inicialise="0">
            <mysql database="db_4gain" password="<password>" server="10.19.2.20" user="<user>" charset="utf8" />
        </database>
        <logging use_file="1" use_syslog="0" >
            <console level="10" />
            <splash level="20" />
            <file level="10" path="$path/var/log/4gain.log" when="d" interval="1" count="7"/>
            <syslog level="30" address_ip="10.19.2.18" address_port="514" />
        </logging>
        <session use_autologin="1">
            <installation uuid="64d5c56c-c938-4198-9e80-ce8fea3810ed" />
            <autologin username="v.tatarnikov" password="test" club_select="2" />
        </session>
        <gui gtk-major="3" gtk-minor="16" gtk-micro="7" date-format="%Y.%m.%d" use_splash="1">
            <Main glade="$path/share/gui/Main.glade" image-auth-logo="$path/share/icons/target.png"
                  image-logo="$path/share/icons/worldwide.png" />
            <MainSplash glade="$path/share/gui/MainSplash.glade" image-splash="$path/share/images/splash.png" />

            <UserManager glade="$path/share/gui/UserManager.glade" image-logo="$path/share/icons/user-17.png" />
            <UserProfile glade="$path/share/gui/UserProfile.glade" image-logo="$path/share/icons/user-4.png" />
            <UserProfilePassword glade="$path/share/gui/UserProfilePassword.glade" image-logo="$path/share/icons/user-5.png" />

            <SaleManager glade="$path/share/gui/SaleManager.glade" />

            <ProductManager glade="$path/share/gui/ProductManager.glade" />
            <ProductManagerDataEntrace glade="$path/share/gui/ProductManagerDataEntrace.glade" />
            <ProductManagerDataPrice glade="$path/share/gui/ProductManagerDataPrice.glade" />
            <ProductManagerDataGroup glade="$path/share/gui/ProductManagerDataGroup.glade" />
            <ProductManagerDataCombinate glade="$path/share/gui/ProductManagerDataCombinate.glade" />

            <ProductManagerEntrace glade="$path/share/gui/ProductManagerEntrace.glade" />
            <ProductSale glade="$path/share/gui/ProductSale.glade" />

            <CashdeskManager glade="$path/share/gui/CashdeskManager.glade" />

            <OperdayManager glade="$path/share/gui/OperdayManager.glade" image-logo="$path/share/icons/dollar-symbol-1.png" />
            <OperdayManagerOpen glade="$path/share/gui/OperdayManagerOpen.glade" image-logo="$path/share/icons/piggy-bank.png" />
            <OperdayManagerClose glade="$path/share/gui/OperdayManagerClose.glade" image-logo="$path/share/icons/piggy-bank-1.png" />
            <OperdayReport glade="$path/share/gui/OperdayReport.glade" image-logo="$path/share/icons/pie-chart.png" />

            <ClubCurrentInformation glade="$path/share/gui/widgets/ClubCurrentInformation.glade" />
            <CashdeskCurrentInformation glade="$path/share/gui/widgets/CashdeskCurrentInformation.glade" />
            <UserCurrentInformation glade="$path/share/gui/widgets/UserCurrentInformation.glade" />
        </gui>
    </configuration>


.. _example-config-4gw:

Конфигурационный фаил 4GW
-------------------------

Данный конфигурационный фаил используется только в среде 4GW, и нигде более.
Он переопределяет параметры основного конфигурационного файла 4GE, для каждного виртаульного хоста (Apache Virtual Host).

Пример "классического" конфигурационного файла:

.. code-block:: xml
    :linenos:

    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <web site_id="1">
            <application import_name="forGain"
                         static_url_path="/static"
                         static_folder="/home/apache/pro-4gain-www/.4gain.web/static"
                         static_folder_master="/home/apache/pro-4gain-www/.4gain/share/static"
                         template_folder="/home/apache/pro-4gain-www/.4gain.web/templates/default"
                         template_folder_master="/home/apache/pro-4gain-www/.4gain/share/templates/default"/>

            <!-- Использовать ли внишние аналитические сервисы (применяется в шаблонах) -->
            <analytics-google enable="True" />
            <analytics-yandex enable="True" />

            <!-- Идентификатор клуба при использовании на сайте информации о "клубе" Interfaces.MySQL.Schema.Club [1] и WEB.Module.Club [2] -->
            <module-club club_id="1" />

            <!-- Определение ключа к функциям google api, применяемых к примеру в WEB.ModuleContact [3] -->
            <google-api gmap="AIzaSyBUxH5_DlaI8DpyfOR-wVPlb_nOFKNR-ew" />
        </web>
    </configuration>

.. rubric:: Сноски
.. [1] :ref:`module-interfaces-mysql-schema-club`
.. [2] :ref:`module-web-modules-club`
.. [3] :ref:`module-web-modules-contacts`


Дополнительную информацию по использованию второго конфигурационного файла можно посмотреть в исходном коде :ref:`module-interfaces-config`, а также в :ref:`module-web-application`.