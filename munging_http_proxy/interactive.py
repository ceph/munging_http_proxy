from . import wsgi
import code
import gevent
import gevent.coros
import readline
import rlcompleter
readline.__name__  # silence pyflakes
rlcompleter.__name__  # silence pyflakes


class InteractiveMunger(object):
    def __init__(self):
        self.local = {}
        self.lock = gevent.coros.Semaphore()

    def munge(self, req):
        with self.lock:
            self.local.update(
                req=req,
                resp=None,
                )
            code.interact(
                banner=('Interactive HTTP proxy. '
                        + 'Mutate req, or set resp to a webob Response.\n'
                        + 'Press control-D to exit...'),
                local=self.local,
                )
            return self.local.get('resp')


def main():
    import gevent.monkey
    gevent.monkey.patch_all()

    import gevent.pywsgi

    inter = InteractiveMunger()

    print 'Serving on 8088...'
    proxy = wsgi.MungingHTTPProxy(munge=inter.munge)
    try:
        gevent.pywsgi.WSGIServer(('0.0.0.0', 8088), proxy.wsgi).serve_forever()
    except KeyboardInterrupt:
        pass
