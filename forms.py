from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, IPAddress

class UsernameForm(FlaskForm):
    username = StringField('Login PPPoE', validators=[DataRequired(),Length(min=2, max=50)])
    ip = StringField('Juniper IP', validators=[IPAddress(ipv4=True, ipv6=False, message='Invalid IP address')])
    submit = SubmitField('Connect')