from flask import Flask
from models import db
from routes import draft_routes, hotel_routes, swagger_routes, user_routes


def setup_routes(app: Flask):
    app.register_blueprint(draft_routes.bp)
    app.register_blueprint(hotel_routes.bp)
    app.register_blueprint(swagger_routes.bp)
    app.register_blueprint(user_routes.bp)
