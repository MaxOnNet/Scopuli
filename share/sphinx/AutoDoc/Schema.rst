.. _module-share_sphinx_autodoc_schema:

share.sphinx.AutoDoc.Schema
===========================

Класс помощник, раскладывает столбцы и связи ORM SqlAlchemy в удобночитаемые таблицы.

Для использования в conf.py Sphinx'a вписываем следующие функции:

.. code-block:: python
    :linenos:

    def autodoc_skip_member(app, what, name, obj, skip, options):
        from share.sphinx.AutoDoc.Schema import Schema as AutoDocSchema

        if name in ["_sa_class_manager"]:
            return True

        if AutoDocSchema(object=obj).has_schema_attr():
            return True


    def autodoc_process_docstring(app, what, name, obj, options, lines):
        from share.sphinx.AutoDoc.Schema import Schema as AutoDocSchema

        if what in ["class"]:
            ads = AutoDocSchema(object=obj)

            if ads.has_schema():
                ads.parse_table()
                ads.parse_columns()
                ads.render(lines=lines)

    def setup(app):
        app.connect('autodoc-skip-member', autodoc_skip_member)
        app.connect('autodoc-process-docstring', autodoc_process_docstring)

.. automodule:: share.sphinx.AutoDoc.Schema
    :members:
    :undoc-members:
    :private-members:
