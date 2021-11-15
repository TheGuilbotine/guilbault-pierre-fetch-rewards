from flask_wtf import FlaskForm
from wtforms import DateField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

validate = [DataRequired()]


class Transaction(FlaskForm):
    payer = StringField("Payer", validate)
    points = IntegerField("Points", validate)
    timestamp = DateField("Timestamp", validate)
    submit = SubmitField("Submit")
