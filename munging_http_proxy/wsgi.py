import urlparse
import webob
import webob.exc
import wsgiproxy.exactproxy
import wsgiref.util


class ImATeaPotError(webob.exc.HTTPClientError):
    """
    This is an intentionally funky response to let you know it's this
    munging proxy doing evil things, and not the origin server.
    """
    code = 418
    title = "I'm a teapot"
    explanation = ("Munging proxy is doing great evil.")


class MungingHTTPProxy(object):
    def __init__(self, munge):
        self.munge = munge

    def wsgi(self, environ, start_response):
        req = webob.Request(environ)
        if req.method == 'CONNECT':
            # we can't handle ssl sanely, so refuse to tunnel
            return ImATeaPotError()(environ, start_response)

        assert wsgiref.util.guess_scheme(req.environ) == 'http'
        assert 'HTTP_HOST' in req.environ
        host = req.environ['HTTP_HOST']
        try:
            (host, port) = host.split(':', 1)
        except ValueError:
            port = '80'

        urlinfo = urlparse.urlsplit(req.environ['PATH_INFO'])
        assert urlinfo.scheme == 'http'
        assert urlinfo.netloc != ''
        if not urlinfo.netloc:
            urlinfo.netloc = req.environ['HTTP_HOST']
        req.environ['PATH_INFO'] = urlparse.urlunsplit((
            '',
            '',
            urlinfo.path,
            urlinfo.query,
            urlinfo.fragment,
            ))

        req.environ.update(
            SERVER_NAME=host,
            SERVER_PORT=port,
            )
        resp = self.munge(req)
        if resp is None:
            resp = req.get_response(wsgiproxy.exactproxy.proxy_exact_request)
        return resp(environ, start_response)
