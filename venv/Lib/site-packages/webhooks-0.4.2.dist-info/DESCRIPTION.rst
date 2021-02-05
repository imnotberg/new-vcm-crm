===============================
webhooks
===============================

.. image:: https://pypip.in/d/webhooks/badge.png
        :target: https://pypi.python.org/pypi/webhooks

.. image:: https://badge.fury.io/py/webhooks.png
    :target: https://badge.fury.io/py/webhooks

.. image:: https://travis-ci.org/pydanny/webhooks.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/webhooks

.. image:: https://pypip.in/wheel/webhooks/badge.png
    :target: https://pypi.python.org/pypi/webhooks/
    :alt: Wheel Status

Python + Webhooks Made Easy

* Free software: BSD license
* Documentation: http://webhooks.rtfd.org.

**WARNING** This project is in a pre-alpha state. It's not ready for use on ANYTHING.

Python Versions
----------------

Currently works in:

    * Python 2.7
    * Python 3.3

Existing Features
------------------

* Easy to integrate into any package or project
* Comes with several built-in senders for synchronous webhooks.
* Comes with a RedisQ-powered asynchronous webhook.
* Extendable functionality through the use of custom senders and hash functions.

Planned Features
-----------------

* Comes with many built-in senders for synchronous and asynchronous webhooks.
* Special functions for combining multiple sends of identical payloads going to one target into one.
* Follows http://resthooks.org patterns
* Great documentation
* Compatibility with PyPy

Usage
-----

Follow these easy steps:

1. Import the ``webhook`` decorator.
2. Define a function that returns a JSON-serializable dictionary or iterable.
3. Add the ``webhook`` decorator and pass in a ``sender_callable``.
4. Call the function!

Synchronous example (async examples to come soon):

.. code-block:: python

    >>> from webhooks import webhook
    >>> from webhooks.senders import targeted

    >>> @webhook(sender_callable=targeted.sender)
    >>> def basic(url, wife, husband):
    >>>     return {"husband": husband, "wife": wife}

    >>> r = basic(url="http://httpbin.org/post", husband="Danny", wife="Audrey")
    >>> import pprint
    >>> pprint.pprint(r)
    {'attempt': 1,
    'hash': '29788eb987104b8a87d201292fa459d9',
    'husband': 'Danny',
    'response': b'{\n  "args": {},\n  "data": "",\n  "files": {},\n  "form": {\n    "attempt": "1",\n    "hash": "29788eb987104b8a87d201292fa459d9",\n    "husband": "Danny",\n    "url": "http://httpbin.org/post",\n    "wife": "Audrey"\n  },\n  "headers": {\n    "Accept": "*/*",\n    "Accept-Encoding": "gzip, deflate",\n    "Connection": "close",\n    "Content-Length": "109",\n    "Content-Type": "application/x-www-form-urlencoded",\n    "Host": "httpbin.org",\n    "User-Agent": "python-requests/2.3.0 CPython/3.3.5 Darwin/12.3.0",\n    "X-Request-Id": "d25119e4-08ba-4523-abc4-b9a9ac10225b"\n  },\n  "json": null,\n  "origin": "108.185.146.101",\n  "url": "http://httpbin.org/post"\n}',
    'status_code': 200,
    'url': 'http://httpbin.org/post',
    'wife': 'Audrey'}



Projects Powered by Webhooks
----------------------------

* https://github.com/pydanny/dj-webhooks




History
-------

0.4.2 (2014-05-22)
+++++++++++++++++++

* Convert python-requests bytes to string when using Python 3

0.4.1 (2014-05-22)
+++++++++++++++++++

* Replaced `json262` with `standardjson` package.

0.4.0 (2014-05-20)
++++++++++++++++++

* Replaced `utils.encoders` with `json262` package.
* utf-8 encoding everywhere
* Add `from `__future__ import absolute_import` everywhere.

0.3.2 (2014-05-17)
++++++++++++++++++

* Brought in simplified `cached_property` decorator


0.3.1 (2014-05-15)
++++++++++++++++++

* Added more Senderable attributes to make it easier to track what's going on.
* Added the missing webhooks.sender package to setup.py.


0.3.0 (2014-05-14)
++++++++++++++++++

* Added extensible Senderable class to expedite creating new senders.
* Added async_redis sender.
* Added travis-ci.

0.2.0 (2014-05-13)
++++++++++++++++++

* Added functioning hook decorator.
* Ramped up test coverage.
* Hash functions placed in their own module.
* Cleaned up JSON encoder thanks to Audrey Roy Greenfeld!

0.1.0 (2014-05-07)
++++++++++++++++++

* First release on PyPI.

