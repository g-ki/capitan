import os
import logging
from flask import Flask, g
from werkzeug.utils import find_modules, import_string

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

def create_app(config=None):
    app = Flask('capitan', instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config.update(config or {})

    register_blueprints(app)
    app.logger.addHandler(stream_handler)

    return app


def register_blueprints(app):
    for name in find_modules('capitan.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            url_prefix = mod.url_prefix if hasattr(mod, 'url_prefix') else None
            app.register_blueprint(mod.bp, url_prefix=url_prefix)
    return None
