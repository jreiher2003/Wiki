from flask_wtf import Form 
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(Form):
    username = TextField('username', validators=[DataRequired(), Length(min=3, max=25)])
  