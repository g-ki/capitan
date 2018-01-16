import os
from flask import Flask, g
from werkzeug.utils import find_modules, import_string

import logging
logging.basicConfig(level=logging.DEBUG)

def create_app(config=None):
    app = Flask('capitan')

    app.config.update(config or {})

    app.secret_key = "Mf\xf2\x94 \xb2^\x81\x92\xb2l\x8d\xc9]'\t\x86\xb9\xb4\xaa\xcc2\x01\xfe"

    register_blueprints(app)

    return app


def register_blueprints(app):
    for name in find_modules('capitan.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            url_prefix = mod.url_prefix if hasattr(mod, 'url_prefix') else None
            app.register_blueprint(mod.bp, url_prefix=url_prefix)
    return None
