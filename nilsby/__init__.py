import types

from pyramid.events import NewRequest
from pyramid.events import subscriber

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

import nilsby.util
from nilsby.models import initialize_sql

@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    request.is_logged_in = types.MethodType(nilsby.util.is_logged_in, request)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    session_factory = UnencryptedCookieSessionFactoryConfig('nilsbysite')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'nilsby:static', cache_max_age=3600)
    
    # Auth routes
    config.add_route('user_new', '/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # Forum routes
    config.add_route('forum_index', '/forum')
    config.add_route('forum_view', '/forum/view/{id}')
    config.add_route('forum_post', '/forum/post')
    config.add_route('forum_reply', '/forum/reply/{post_id}')

    # User routes
    config.add_route('user_index', '/users')
    config.add_route('user_view', '/user/view/{id}')
    
    # Home route
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

