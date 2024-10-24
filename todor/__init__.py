from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../static')

    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        REDIS_URL='redis://localhost:6379'
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from . import todo
    app.register_blueprint(todo.bp)

    from . import auth
    app.register_blueprint(auth.bp, name='auth_bp')

    from . import adm
    app.register_blueprint(adm.bp, name='adm_bp')

    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app