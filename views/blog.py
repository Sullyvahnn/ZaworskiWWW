from copy import deepcopy
from datetime import datetime

from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify
from flask_security import current_user, login_required
from sqlalchemy.exc import OperationalError

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from models import Article, db
from views.main import get_logged_user

bp = Blueprint('bp_blog', __name__)


# Show list of articles
@bp.route('/blog', methods=['GET'])
@bp.route('/blog/page/<int:page>', methods=['GET'])
def blog_get(page=1, total_pages=1):
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('blog.html', page=page,
                            total_pages=total_pages, articles=articles, username=get_logged_user().username)


# Show article
@bp.route('/blog/show/<int:article_id>', methods=['GET'])
def blog_show_get(article_id=0):
    article = Article.query.get_or_404(article_id)
    return render_template('blog_show.html', article=article, username=get_logged_user().username)


# Add new article
@bp.route('/blog/add', methods=['GET', 'POST'])
@login_required
def blog_add_get_post():
    errors = {}
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not errors:
            # Tu dodajesz artykuł do bazy danych
            new_article = Article(title=title, content=content, user_id=get_logged_user().id)
            db.session.add(new_article)
            db.session.commit()
            return redirect("/blog")

    return redirect("/blog")


# Edit article
@bp.route('/blog/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def blog_edit_get_post(article_id=0):
    article = Article.query.get_or_404(article_id)

    # Access control: only the author can edit
    if article.user_id != current_user.id:
        flash("Nie masz uprawnień do edycji tego artykułu.", "danger")
        return redirect(url_for("bp_blog.blog_show_get", article_id=article.id))

    errors = {}

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        # Basic validation
        if not title:
            errors["title"] = "Tytuł jest wymagany."
        if not content:
            errors["content"] = "Treść jest wymagana."

        if not errors:
            article.title = title
            article.content = content
            article.modified_at = datetime.now()

            db.session.commit()
            flash("Artykuł został zaktualizowany.", "success")
            return redirect(url_for("bp_blog.blog_show_get", article_id=article.id))
        else:
            flash("Popraw błędy w formularzu.", "danger")

    return render_template(
        "blog_edit.html",
        article=article,
        errors=errors
    )


# Delete article
@bp.route('/blog/delete/<int:article_id>', methods=['GET'])
@login_required
def blog_delete_get(article_id=0):
    pass

@bp.route('/blog/add_window')
@login_required
def blog_add_window(article_id=0):
    return render_template('blog_add.html', username=get_logged_user().username)

@bp.route('/blog/edit_window/<int:article_id>', methods=['GET'])
def blog_edit_window(article_id=0):
    article = Article.query.get_or_404(article_id)
    errors = {}
    return render_template('blog_edit.html', article=article,
                           username=get_logged_user().username, errors=errors)