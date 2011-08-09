========================================================
 Munging HTTP Proxy -- Manipulate HTTP requests easily.
========================================================

``munging_http_proxy`` lets you easily modify or intercept HTTP
requests passing through the proxy. All you need to do is write a
Python function that takes a WebOb_ ``Request``, and either mutates it
and returns ``None`` (request will be passed on, and the response from
the server relayed to the client), or directly returns a suitable
WebOb ``Response`` (server will never be contacted).

.. _WebOb: http://webob.org/

Note that some of the fields of a WebOb ``Request`` are read-only
properties. For example, you cannot set ``req.path``, you'll have to
set ``req.path_info`` and/or ``req.script_name``.

``munging_http_proxy`` also contains an interactive mode, where every
request is explorable in an interactive Python session. In this mode,
use ``req`` to access the ``Request``, and set ``resp`` if you wish to
directly return a specific ``Response``. For convenience, any other
variables you set are remembered between the requests.


To get started, type::

	./bootstrap

And for interactive mode, type::

	./virtualenv/bin/interactive-http-proxy

Now you can make requests using the HTTP proxy. For example (in
another window)::

	http_proxy=http://localhost:8088/ wget -nv -O- 'http://example.com/'
