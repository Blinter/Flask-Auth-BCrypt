from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField


class AddUserForm(FlaskForm):
    """Form for adding User."""

    """Must be filled"""
    username = StringField("User Name", [
        validators.Length(1, 20),
        validators.InputRequired(message='User Name cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'User Name'
    })

    """Must be filled"""
    password = PasswordField("Password", [
        validators.Length(1, 20),
        validators.InputRequired(message='Password cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Password'
    })

    """Must be filled"""
    email = StringField("Email", [
        validators.Length(3, 50),
        validators.InputRequired(message='Email cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Email'
    })

    """Must be filled"""
    first_name = StringField("First Name", [
        validators.Length(1, 30),
        validators.InputRequired(message='First Name cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'First Name'
    })

    """Must be filled"""
    last_name = StringField("Last Name", [
        validators.Length(1, 30),
        validators.InputRequired(message='Last Name cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Last Name'
    })

    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary '
                                                         'btn-lg '
                                                         'btn-block'})


class LoginUserForm(FlaskForm):
    """Form for Logging into user."""

    """Must be filled"""
    username = StringField("User Name", [
        validators.Length(1, 20),
        validators.InputRequired(message='User Name cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'User Name'
    })

    """Must be filled"""
    password = PasswordField("Password", [
        validators.Length(1, 20),
        validators.InputRequired(message='Password cannot be empty'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Password'
    })

    submit = SubmitField('Login', render_kw={
        'class': 'btn btn-primary btn-lg btn-block'})


class AddFeedbackForm(FlaskForm):
    """Form for Adding Feedback for User."""

    """Must be filled"""
    title = StringField("Title", [
        validators.Length(1, 100),
        validators.InputRequired(message='Title Size Error.'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Title'
    })

    """Must be filled"""
    content = PasswordField("Content", [
        validators.Length(1, 10000),
        validators.InputRequired(message='Content Size Error'),
    ], render_kw={
        'class': "form-control form-control-lg",
        'placeholder': 'Content'
    })

    submit = SubmitField('Add Feedback', render_kw={
        'class': 'btn btn-primary btn-lg btn-block'})
