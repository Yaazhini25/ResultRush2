from flask import Flask, request
import time
from .models import init_db


def create_app():
    app = Flask(__name__)

    # initialize DB using app config
    init_db(app)

    from .routes import routes
    app.register_blueprint(routes)

    @app.before_request
    def before_request():
        request.start_time = time.time()

    return app