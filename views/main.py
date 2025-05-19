from flask import render_template, Blueprint, request

from models import User

main = Blueprint('main', __name__)

@main.route('/?<int:user_id>', methods=['GET'])
def index(user_id):
    username = User.query.filter_by(id=user_id).first().username
    return render_template('base.html', username=username)

@main.route('/')
def serve_base():
    return render_template("base.html", username="Not Logged in")

