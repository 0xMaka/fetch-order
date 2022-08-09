from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FetchOrder(FlaskForm):
  chainId = StringField('chainId', validators=[DataRequired()])
  address = StringField('Address', validators=[DataRequired()])
  submit = SubmitField('Return Order(s)')
