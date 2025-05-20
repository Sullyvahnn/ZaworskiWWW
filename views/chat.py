from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify
from flask_security import current_user, login_required
from sqlalchemy import select, asc
from sqlalchemy.exc import OperationalError
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from models import User, db, Message

bp = Blueprint('chat', __name__)


# Show chat window
@bp.route('/chat', methods=['GET'])
@login_required
def chat_get():
    return render_template('chat.html', username=current_user.username)


# Get list of messages
@bp.route('/chat/messages/<int:message_id>', methods=['GET'])
@bp.route('/chat/messages', methods=['GET'])
# @login_required
def chat_messages_get():
    message_id = request.args.get('message_id', type=int)
    limit = 20

    if message_id:
        # Get the timestamp of the message with the given ID
        ref_message = Message.query.get(message_id)
        if not ref_message:
            return jsonify({"error": "Message ID not found"}), 404

        messages = Message.query.filter(Message.created_at > ref_message.created_at) \
            .order_by(asc(Message.created_at)) \
            .limit(limit) \
            .all()
    else:
        # Get the latest 20 messages sorted from oldest to newest
        messages = Message.query.order_by(Message.created_at.desc()) \
            .limit(limit) \
            .all()
        messages = list(reversed(messages))  # So oldest to newest

    result = [
        {
            "id": msg.id,
            "user_id": msg.user_id,
            "username": msg.username,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in messages
    ]

    return jsonify({"count": len(result), "result": result}), 200


# Add new message
@bp.route('/chat/messages', methods=['POST'])
@login_required
def chat_messages_post():
    data = request.get_json()
    print(data)
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request body"}), 400

    try:
        new_msg = Message(
            user_id=current_user.id,  # Placeholder: you should handle actual user logic
            username=current_user.username,
            content=data['content'],
        )

        db.session.add(new_msg)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Edit message
@bp.route('/chat/messages/<int:message_id>', methods=['PUT'])
@login_required
def chat_messages_put(message_id=0):
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request body"}), 400

    message = Message.query.get(message_id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    # Simulated current user (you can replace this with actual user logic)
    current_user_id = 1

    if message.user_id != current_user_id:
        return jsonify({"error": "You are not the author of this message"}), 400

    try:
        message.content = data['content']
        message.modified_at = datetime.utcnow()
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Delete message
@bp.route('/chat/messages/<int:message_id>', methods=['DELETE'])
@login_required
def chat_messages_delete(message_id=0):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    # Simulated current user (replace with real auth logic)
    current_user_id = 1

    if message.user_id != current_user_id:
        return jsonify({"error": "You are not the author of this message"}), 400

    try:
        db.session.delete(message)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Sample endpoint
@bp.route('/chat/test', methods=['GET'])
@login_required
def chat_test_get():
    try:
        limit = int(request.args.get('limit'))
    except (ValueError, TypeError):
        limit = 0

    # every method is described here: https://docs.sqlalchemy.org/en/14/orm/query.html
    users = User.query.add_columns(User.id, User.email, User.username).order_by(User.id.desc())
    if limit > 0:
        users = users.limit(limit)
    users = users.all()

    results = []
    for user in users:
        results.append({'id': user.id, 'email': user.email, 'username': user.username})

    return jsonify(results)