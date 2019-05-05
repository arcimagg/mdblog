from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from .database import articles

flask_app = Flask(__name__)
flask_app.secret_key = b"?K'0\x02\x9cf\xeaE^\xc49\xd7S&\t1\x95\x0cara\xb7\xdf"

# Route view

@flask_app.route("/")
def view_welcome_page():
    return render_template("welcome_page.jinja")

@flask_app.route("/about/")
def view_about():
    return render_template("about.jinja")

@flask_app.route("/admin/")
def view_admin():
	if "logged" not in session:
		return redirect(url_for("view_login"))
	return render_template("admin.jinja")

# Artiles

@flask_app.route("/articles/")
def view_articles():
    return render_template("articles.jinja", articles=articles.items())

@flask_app.route("/articles/<int:art_id>")
def view_article(art_id):
    article = articles.get(art_id) # get je funkcia dictionary ak nenajde take id tak vrati none
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

# Login

@flask_app.route("/login/", methods=["GET"])
def view_login():
	return render_template("login.jinja")

@flask_app.route("/login/", methods=["POST"])
def login_user():
	username = request.form["username"]
	password = request.form["password"]
	if username == "admin" and password == "admin":
		session["logged"] = True
		return redirect(url_for("view_admin"))
	else:
		return redirect(url_for("view_login"))

@flask_app.route("/logout/", methods=["POST"])
def logout_user():
	session.pop("logged")
	return redirect(url_for("view_welcome_page"))