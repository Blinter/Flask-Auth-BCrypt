"""User Authentication"""
from flask import Flask, redirect, request, render_template, flash, session

from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm
from flask_bcrypt import Bcrypt


# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'test_debug_form'


@app.errorhandler(401)
def page_not_found(e):
    """Default 401 Page"""
    session_user = session.get('username', False)
    if session_user:
        user_exists = db.session.query(db.session.query(User).filter_by(
            username=session_user).exists()).scalar()
        if user_exists:
            user = db.get_or_404(User, session_user)
            flash(f"Page not Authorized! " + request.url, 'danger')
            return render_template("user_info.html", user=user)
        else:
            flash(f"Incorrect User Token", 'danger')
            session.pop('username', None)
            return redirect("/")
    flash("Page not found! " + request.url, 'danger')
    return render_template('401.html')


@app.errorhandler(404)
def page_not_found(e):
    """Default 404 Page"""
    session_user = session.get('username', False)
    if session_user:
        user_exists = db.session.query(db.session.query(User).filter_by(
            username=session_user).exists()).scalar()
        if user_exists:
            user = db.get_or_404(User, session_user)
            flash(f"Page not found! " + request.url, 'danger')
            return render_template("user_info.html", user=user)
        else:
            flash(f"Incorrect User Token", 'danger')
            session.pop('username', None)
            return redirect("/")
    flash("Page not found! " + request.url, 'danger')
    return render_template('404.html')


@app.route("/")
def home():
    """Register Redirect"""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Form Displayed (GET, POST)
    Register New User"""
    session_user = session.get('username', False)
    if session_user:
        user_exists = db.session.query(db.session.query(User).filter_by(
            username=session_user).exists()).scalar()
        if user_exists:
            user = db.get_or_404(User, session_user)
            flash(f"Welcome {user.fullname}!", 'primary')
            return render_template("user_info.html", user=user)
        else:
            flash(f"Incorrect User Token", 'danger')
            session.pop('username', None)
            return redirect("/")
    form = AddUserForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # Check if user exists.
        if db.session.query(db.session.query(User).filter_by(
                username=user_name).exists()).scalar():
            flash(f"Username already taken!", 'primary')
            return render_template("user_register_form.html", form=form)
        if db.session.query(db.session.query(User).filter_by(email=email)
                            .exists()).scalar():
            flash(f"Email already taken!", 'primary')
            return render_template("user_register_form.html", form=form)
        user = User(username=user_name,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

        db.session.add(user.hash_password())
        db.session.commit()
        session['username'] = user.username
        session.modified = True
        flash("New user added successfully!", 'success')
        return redirect("/secret")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field} {error}", 'danger')
        return render_template("user_register_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Form is displayed for unauthenticated user to log in. (GET, POST)
    Proper messages are flashed based on incorrect details.
    """
    form = LoginUserForm()
    if form.validate_on_submit():
        user_name = form.username.data
        user_exists = db.session.query(db.session.query(User).filter_by(
            username=user_name).exists()).scalar()
        if not user_exists:
            flash(f"Incorrect Username", 'danger')
            return render_template("user_login_form.html", form=form)
        password = form.password.data
        user = db.get_or_404(User, user_name)
        # print("check: " + str(password) + "===" + str(user.password))
        user = user.authenticate(password)
        if not user:
            flash(f"Incorrect Password", 'danger')
            return render_template("user_login_form.html", form=form)
        session['username'] = user_name
        return redirect("/secret")
    else:
        session_user = session.get('username', False)
        if session_user:
            db_username = db.get_or_404(User, session_user)
            flash(f"Welcome {db_username.fullname}!", 'primary')
            return render_template("user_info.html", user=db_username)

        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error for field '{field}': {error}", 'danger')
        return render_template("user_login_form.html", form=form)


@app.route("/secret", methods=["GET"])
def secret():
    """
    Exercise Test (GET)
    """
    session_user = session.get('username', False)
    if session_user:
        user_exists = db.session.query(db.session.query(User).filter_by(
            username=session_user).exists()).scalar()
        if user_exists:
            user = db.get_or_404(User, session_user)
            flash(f"Welcome {user.fullname}!", 'primary')
            return render_template("user_info.html", user=user)
        else:
            flash(f"Incorrect User Token", 'danger')
            session.pop('username', None)
            return redirect("/")
    else:
        flash("You don't have access!", 'danger')
        return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout():
    """Clear User Auth Session (GET)"""
    session.pop('username', None)
    return redirect("/")


@app.route("/users/<string:username>", methods=["GET"])
def user_info_get(username):
    """Feedback Add"""
    session_user = session.get('username', False)
    if not session_user or session_user != username:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    db_username = db.get_or_404(User, username)
    flash(f"Welcome {db_username.fullname}!", 'primary')
    return render_template("user_info.html", user=db_username)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET"])
def feedback_edit_get(feedback_id):
    """Feedback Edit (GET)"""
    session_user = session.get('username', False)
    if not session_user:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    feedback_exists = db.session.query(db.session.query(Feedback).filter_by(
        id=feedback_id).exists()).scalar()
    if not feedback_exists:
        flash("Feedback does not exist!", 'danger')
        return render_template("user_info.html",
                               user=db.get_or_404(User, session_user))
    form = AddFeedbackForm()
    db_feedback = db.get_or_404(Feedback, feedback_id)
    if session_user == db_feedback.username.username:
        flash(f"Welcome {db_feedback.username.fullname}! Edit your feedback?",
              'primary')
        return render_template("feedback_edit.html",
                               feedback=db_feedback,
                               form=form)
    else:
        flash("The selected feedback cannot be edited!", 'danger')
        return render_template("401.html",
                               user=db.get_or_404(User, session_user))


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def feedback_delete_post(feedback_id):
    """Feedback Delete (POST)"""
    session_user = session.get('username', False)
    if not session_user:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    feedback_exists = db.session.query(db.session.query(Feedback).filter_by(
        id=feedback_id).exists()).scalar()
    if not feedback_exists:
        flash("Feedback does not exist!", 'danger')
        return render_template("user_info.html", user=db.get_or_404(User,
                                                                    session_user
                                                                    ))
    db_feedback = db.get_or_404(Feedback, feedback_id)
    if session_user == db_feedback.username.username:
        db.session.delete(db_feedback)
        db.session.commit()
        flash(f"Feedback {feedback_id} deleted!", 'danger')
        return render_template("user_info.html", user=db.get_or_404(User,
                                                                    session_user
                                                                    ))
    else:
        flash("Feedback cannot be deleted!", 'danger')
        return render_template("user_info.html", user=db.get_or_404(User,
                                                                    session_user
                                                                    ))


@app.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def feedback_update_post(feedback_id):
    """Feedback Update (POST)"""
    session_user = session.get('username', False)
    if not session_user:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    feedback_exists = db.session.query(db.session.query(Feedback).filter_by(
        id=feedback_id).exists()).scalar()
    if not feedback_exists:
        flash("Feedback does not exist!", 'danger')
        form = AddFeedbackForm()
        return render_template("user_info.html", form=form,
                               user=db.get_or_404(User, session_user))
    db_feedback = db.get_or_404(Feedback, feedback_id)
    if session_user == db_feedback.username.username:
        form = AddFeedbackForm()
        if not form.validate_on_submit():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error for field '{field}': {error}", 'danger')
            return render_template("feedback_edit.html", form=form,
                                   feedback=db_feedback)
        db_feedback.title = request.form.get('title', None)
        db_feedback.content = request.form.get('content', None)
        db_feedback.verified = True
        db.session.commit()
        flash(f"Feedback {feedback_id} updated!", 'info')
        return render_template("user_info.html", user=db.get_or_404(User,
                                                                    session_user
                                                                    ))
    else:
        flash("Feedback cannot be modified!", 'danger')
        return render_template("user_info.html",
                               user=db.get_or_404(User, session_user))


@app.route("/users/<string:username_get>/feedback/add", methods=["GET"])
def feedback_add_get(username_get):
    """Feedback Add (Get)"""
    session_user = session.get('username', False)
    if not session_user or session_user != username_get:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    db_username = db.get_or_404(User, username_get)
    flash(f"Welcome {db_username.fullname}! Add Feedback?", 'primary')
    return render_template("feedback_add.html",
                           form=AddFeedbackForm(),
                           username=db_username.username)


@app.route("/users/<string:username_get>/feedback/add", methods=["POST"])
def feedback_add_post(username_get):
    """Feedback Add (Post)"""
    session_user = session.get('username', False)
    if not session_user or username_get != session_user:
        flash("You don't have access!", 'danger')
        return render_template("user_login_form.html", form=LoginUserForm())
    form = AddFeedbackForm()
    if form.validate_on_submit():
        title = request.form.get('title', None)
        content = request.form.get('content', None)
        new_feedback = Feedback(title=title, content=content,
                                user=session_user)
        db.session.add(new_feedback)
        db.session.commit()
        flash(f"Feedback {new_feedback.id} updated!", 'info')
        return render_template("user_info.html", user=db.get_or_404(User,
                                                                    session_user
                                                                    ))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error for field '{field}': {error}", 'danger')
        return render_template("feedback_add.html", form=form)
