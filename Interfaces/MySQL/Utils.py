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


def transliterate(string):
    """
        Функция транслитиризации.
        
        :param string: Строковое значение на русском языке
        :type string: String
        :return: Строковое значение в ANSII
        :rtype: String
    """
    import re
    
    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E', }

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Я': u'Ya', }

    lower_case_letters = {
                        u'а': u'a',
                        u'б': u'b',
                        u'в': u'v',
                        u'г': u'g',
                        u'д': u'd',
                        u'е': u'e',
                        u'ё': u'e',
                        u'ж': u'zh',
                        u'з': u'z',
                        u'и': u'i',
                        u'й': u'y',
                        u'к': u'k',
                        u'л': u'l',
                        u'м': u'm',
                        u'н': u'n',
                        u'о': u'o',
                        u'п': u'p',
                        u'р': u'r',
                        u'с': u's',
                        u'т': u't',
                        u'у': u'u',
                        u'ф': u'f',
                        u'х': u'h',
                        u'ц': u'ts',
                        u'ч': u'ch',
                        u'ш': u'sh',
                        u'щ': u'sch',
                        u'ъ': u'',
                        u'ы': u'y',
                        u'ь': u'',
                        u'э': u'e',
                        u'ю': u'yu',
                        u'я': u'ya', }

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.iteritems():
        string = re.sub(ur"%s([а-я])" % cyrillic_string, ur'%s\1' % latin_string, string)

    for dictionary in (capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.iteritems():
            string = re.sub(cyrillic_string, latin_string, string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.iteritems():
        string = re.sub(cyrillic_string, latin_string.upper(), string)

    return string


def safe_string(unsafe_string):
    """
        Функция фильтр, очищает строковое значение от спец символов.
        Безопасные символы это буквы, цифры и "-", "_".
        
        :param unsafe_string: Не безопасное строковое значение
        :type unsafe_string: String
        :return: Безопасное строковое значение
        :rtype: String
    """
    import string
    import hashlib
    
    try:
        safechars = string.letters + string.digits + "-_"
        return filter(lambda c: c in safechars, unsafe_string)
    except:
        return hashlib.sha256(unsafe_string).hexdigest()


