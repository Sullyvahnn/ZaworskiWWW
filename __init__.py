from flask import Flask
from flask_login import LoginManager

from models import db, User


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    db.init_app(app)

    # blueprint for auth routes in our app
    from views.blog import bp
    app.register_blueprint(bp)

    # blueprint for non-auth parts of app
    from views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run()