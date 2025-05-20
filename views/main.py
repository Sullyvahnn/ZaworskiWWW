from flask import render_template, Blueprint, request
from flask_login import current_user

from models import User


def get_logged_user():
    if current_user.is_authenticated:
        return current_user
    else:
        return User.query.filter_by(id=1).first()


main = Blueprint('main', __name__)

@main.route('/')
def serve_base():
    return render_template("base.html", username=get_logged_user().username,)


