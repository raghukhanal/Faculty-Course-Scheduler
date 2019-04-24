from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired
from models import Faculty


class LoginForm(FlaskForm):
    user_id = IntegerField("User Id", validators=[DataRequired()])
    pin_number = PasswordField("Pin Number", validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_user_id(self, user_id):
        faculty = Faculty.select().where(user_id == user_id.data)
        if faculty is not None:
            raise ValidationError("Please user a different User Id")
