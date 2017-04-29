import models
import forms

from flask import (Flask, render_template, g, redirect, url_for, flash)
from flask_login import (current_user, login_required, LoginManager,
                         login_user, logout_user)
from flask_bcrypt import check_password_hash

app = Flask(__name__)
app.secret_key = "secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None



@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.DATABASE
    g.db.get_conn()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close connection after each request"""
    g.db.close()
    return response


@app.route("/")
@app.route("/entries")
def index():
    entries = models.Entry.select()
    return render_template("index.html", entries=entries)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username**form.username.data)
        except models.DoesNotExist:
            flash("Username or password is incorrect")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Username or password is incorrect")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/entry/add", methods=["GET", "POST"])
@login_required
def add():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            time_spent=form.time_spent.data,
            material_learned=form.material_learned.data,
            resources_to_remember=form.resources_to_remember.data,
            user=g.user._get_current_object()
        )
        return redirect(url_for("index"))
    return render_template("new.html", form=form)

@app.route("/details/<entry_id>")
def details(entry_id):
    try:
        entry = models.Entry.get(models.Entry.id == entry_id)
        return render_template("detail.html", entry=entry)
    except models.DoesNotExist:
        return "No entry found"


@app.route("/entries/edit/<entry_id>", methods=["GET", "POST"])
@login_required
def edit(entry_id):
    entry = models.Entry.get(models.Entry.id==entry_id)
    if entry:
        form = forms.PostForm()
        if form.validate_on_submit():
            entry.title=form.title.data
            entry.time_spent=form.time_spent.data
            entry.material_learned=form.material_learned.data
            entry.resources_to_remember=form.resources_to_remember.data
            entry.save()
            return redirect(url_for("index"))
    return render_template("edit.html", form=form, entry=entry)


@app.route("/delete/<entry_id>")
@login_required
def delete(entry_id):
    entry = models.Entry.get(models.Entry.id==entry_id)
    entry.delete_instance()
    return redirect(url_for("index"))    

if __name__ == "__main__":
    models.initialize()
    app.run(debug=True)