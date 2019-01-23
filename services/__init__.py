# author: tiankai
# copywrite 2019

import os
from datetime import timedelta

from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='services',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # refresh the cache
    app.send_file_max_age_default = timedelta(seconds=1)
    app.config['JSON_AS_ASCII'] = False

    # auth
    from . import auth
    app.register_blueprint(auth.bp)

    # download
    from . import downloadWK
    app.register_blueprint(downloadWK.bp)

    return app
