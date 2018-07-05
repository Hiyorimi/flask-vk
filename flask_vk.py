# -*- coding: utf-8 -*-
"""
    flask_vk
    ~~~~~~~~~~~~~~~~

    Python vk module as a flask extension

    :copyright: (c) 2018 by Kirill Malev.
    :license: WTFPL, see LICENSE for more details.
"""
from __future__ import absolute_import

import vk
from flask import current_app

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class VKAPI(object):
    """
    This is a Flask extension for handling VK.com api requests
    inside your flask application. Depending on how you initialize the
    object it is usable right away or will attach as needed to a
    Flask application.

    There are two usage modes which work very similarly.  One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        vk = VKAPI(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        vk = VKAPI()
        def create_app():
            app = Flask(__name__)
            vk.init_app(app)
            return app

    In the latter case a :meth:`flask.Flask.app_context` has to exist.

    After creation you can access session in any view, for example::

    server_time = vk.api.getServerTime(v=5.71)

    """
    def __init__(self, app=None, token=None):
        self.app = app
        self.token = token
        self.token_is_set = False
        self.VK_APP_CLIENT_ID = None
        if token is not None:
            self.token_is_set = True
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if (hasattr(app.config, 'VK_API_ACCESS_TOKEN') or app.config['VK_API_ACCESS_TOKEN'] is not None):
            if self.token is None:
                self.token = app.config['VK_API_ACCESS_TOKEN']
                self.token_is_set = True
        else:
            if self.token is None:
                raise ValueError("You need to pass token when initializing VKAPI")
        if hasattr(app.config, 'VK_APP_CLIENT_ID') or app.config['VK_API_ACCESS_TOKEN'] is not None:
            self.VK_APP_CLIENT_ID = app.config['VK_APP_CLIENT_ID']
        else:
            ValueError("Need to setup VK_APP_CLIENT_ID config option")
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        if self.token_is_set:
            session = vk.Session(access_token=self.token)
            return vk.API(session)
        else:
            raise ValueError("Token is not set")

    def update_token(self, token):
        self.token = token

    def get_auth_link(self):
        url = "http://oauth.vk.com/authorize?client_id={}&scope=ads,wall,offline&response_type=token&redirect_uri=https://oauth.vk.com/blank.html".format(self.VK_APP_CLIENT_ID)
        return url

    def is_session_valid(self):
        try:
            self.api.getServerTime(v=5.71)
            return True
        except:
            return False

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'vk_api'):
            ctx.vk_api._session.requests_session.close()

    @property
    def api(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'vk_api'):
                ctx.vk_api = self.connect()
            return ctx.vk_api
