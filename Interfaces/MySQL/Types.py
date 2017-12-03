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

from Interfaces.MySQL.SQLAlchemy import String, TypeDecorator, type_coerce, func


class PasswordType(TypeDecorator):
    impl = String(40)

    def bind_expression(self, bindvalue):
        """Apply a SQL expression to an incoming cleartext value being
        rendered as a bound parameter.

        For this example, this handler is intended only for the
        INSERT and UPDATE statements.  Comparison operations
        within a SELECT are handled below by the Comparator.

        """
        return func.crypt(bindvalue, func.gen_salt('md5'))

    class comparator_factory(String.comparator_factory):
        def __eq__(self, other):
            """Compare the local password column to an incoming cleartext
            password.

            This handler is invoked when a PasswordType column
            is used in conjunction with the == operator in a SQL
            expression, replacing the usage of the "bind_expression()"
            handler.

            """
            # we coerce our own "expression" down to String,
            # so that invoking == doesn't cause an endless loop
            # back into __eq__() here
            local_pw = type_coerce(self.expr, String)
            return local_pw == func.crypt(other, local_pw)

