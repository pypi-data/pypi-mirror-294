====================================================
objns - Transform a Python dictionary into an object
====================================================

Simple Python utility module that allows to recursively transform any
dictionary or dictionary like object into a Python object with dot notation
access to its attributes.

This is specially helpful when dealing with large configuration files
(from parsing YAML, JSON or TOML) or dealing with a large response from a
server.


Install
=======

.. code-block:: sh

    pip3 install objns

Optionally, install the following package to enable better pretty printing of
an object:

.. code-block:: sh

    pip3 install pprintpp


Usage
=====

Create an object from one or more dictionaries, and set values directly in the
constructor:

.. code-block:: python3

    >>> from objns import Namespace
    >>> ns = Namespace(
    ...     {'one': 100},
    ...     {'two': 300},
    ...     {'two': 400, 'three': {'four': 400}},
    ...     one=200,
    ... )
    >>> ns.two
    400
    >>> ns.one
    200
    >>> ns['two']
    400

Get and set values recursively:

.. code-block:: python3

    >>> ns['two'] = 300
    >>> ns['two']
    300
    >>> ns.two = 700
    >>> ns['two']
    700
    >>> ns.two
    700
    >>> ns.three.four
    400
    >>> ns['three'].four
    400
    >>> ns['three']['four']
    400

Recursively copy an object:

.. code-block:: python3

    >>> nscopy = ns.copy()
    >>> id(ns) == id(nscopy)
    False

Transform back to a dictionary:

.. code-block:: python3

    >>> asdict = dict(ns)
    >>> asdict
    {'one': 200, 'two': 400, 'three': {'four': 400}}
    >>> type(asdict)
    <class 'dict'>

Iterate the object:

.. code-block:: python3

    >>> for key, value in ns:
    ...     print(key, value)
    ...
    one 200
    two 400
    three {'four': 400}

Recursively merge update with other dictionaries:

.. code-block:: python3

    >>> ns.update({
    ...     'one': 'override1',
    ...     'three': {'four': 'override2'},
    ... })
    >>> ns.one
    'override1'
    >>> ns.three.four
    'override2'

Pretty print the data structure:

.. code-block:: python3

    >>> ns
    {'one': 'override1', 'three': {'four': 'override2'}, 'two': 400}
    >>> print(str(ns))
    {'one': 'override1', 'three': {'four': 'override2'}, 'two': 400}

Preservation of source datatype, such as `OrderedDict` and other Mapping
subclasses:

.. code-block:: python3

    >>> nso = Namespace(OrderedDict([('one', 100), ('two', 200)]))
    >>> nso
    OrderedDict([('one', 100), ('two', 200)])
    >>> for key, value in nso:
        ...     print(key, value)
        ...
        one 100
        two 200


Repository
==========

    https://github.com/kuralabs/objns


Changelog
=========

1.0.0 (2021-05-31)
------------------

New
~~~

- Initial release.


License
=======

.. code-block:: text

   Copyright (C) 2017-2021 KuraLabs S.R.L

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
