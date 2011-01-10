from pyramid.config import Configurator

from repoze.zodbconn.finder import PersistentApplicationFinder
from pylonshq.models import appmaker


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    zodb_uri = settings.get('zodb_uri')
    if zodb_uri is None:
        raise ValueError("No 'zodb_uri' in application configuration.")

    finder = PersistentApplicationFinder(zodb_uri, appmaker)
    def get_root(request):
        return finder(request.environ)
    config = Configurator(root_factory=get_root, settings=settings)
    config.add_static_view('static', 'pylonshq:static')
    config.scan('pylonshq')
    config.add_subscriber('pylonshq.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    return config.make_wsgi_app()
