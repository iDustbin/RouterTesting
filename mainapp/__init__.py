from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME1 = "routerTesting.db"

BACKEND_URL = "http://127.0.0.1:8080/"
def create_app():
    app = Flask(__name__, static_url_path='')
    app.config['SECRET_KEY'] = "RandomString"

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME1}'
    db.init_app(app)

    from .viewables import viewables
    # from .auth import auth
    from .sample import sample

    app.register_blueprint(viewables, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(sample, url_prefix='/response')


    with app.app_context():
        db.create_all(app=app)

    return app
