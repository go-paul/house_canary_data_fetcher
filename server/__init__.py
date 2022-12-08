import logging
import os
from logging.config import dictConfig

from flask import Flask
from flask import jsonify
from werkzeug.utils import import_string

from .api import views as api_v1_views
from .utils.exceptions import APIException
from .utils.exceptions import BadRequest

FLASK_SETTINGS_MODULE = os.environ.get('FLASK_SETTINGS_MODULE', 'server.settings.base')


def create_app() -> Flask:
    # Logging
    flask_logger = logging.getLogger('flask')
    settings = import_string(FLASK_SETTINGS_MODULE)
    dictConfig(settings.LOGGING)

    # Create and configure the app
    app = Flask(__name__)
    app.logger = flask_logger
    app.config.from_object(FLASK_SETTINGS_MODULE)

    # API URLS
    app.add_url_rule('/realty', view_func=api_v1_views.RealtyView.as_view(name='realty'))

    @app.errorhandler(APIException)
    def project_errors_handler(e):
        response = {
            'data': {},
            'errors': e.payload,
        }
        return jsonify(response), e.status_code

    return app
