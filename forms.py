from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class loginForm(FlaskForm):

    username = StringField(label="Username: ",
                           validators=[DataRequired()])
    password = PasswordField(label="Password: ",
                             validators=[DataRequired()])
    submit = SubmitField(label="Go!")


class signupForm(FlaskForm):

    firstName = StringField(label="First Name",
                            validators=[DataRequired(), Length(max=32, message="First Name too long.")])
    lastName = StringField(label="Last Name",
                           validators=[DataRequired(), Length(max=32, message="Last Name too long.")])
    username = StringField(label="Username",
                           validators=[DataRequired(), Length(max=16, message="Username can not be longer than 16 Characters!")])
    password = PasswordField(label="Password",
                             validators=[DataRequired(), Length(min=8, max=32, message="Password must be between 8-32 Characters!")])
    confirmPassword = PasswordField(label="Confirm Password",
                                    validators=[DataRequired(), EqualTo('password', message="Passwords must match!")])
    submit = SubmitField(label="Try Free!")
