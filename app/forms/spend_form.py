from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

validate = [DataRequired()]


class Spend(FlaskForm):
    points = IntegerField("Points", validate)
    sunmit = SubmitField("Submit")
