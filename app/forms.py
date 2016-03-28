from flask_wtf import Form 
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignUpForm(Form):
    username = TextField("username", validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField("email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password", message="Passwords didn't match.")])
  

class LoginForm(Form):
    username = TextField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class WikiForm(Form):
    wiki_post = TextAreaField("Wiki Post", validators=[DataRequired()])