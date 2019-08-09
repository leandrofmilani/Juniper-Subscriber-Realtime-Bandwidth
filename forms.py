from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, IPAddress

class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=40)])
    ip = StringField('Ip do concentrador', validators=[IPAddress(ipv4=True, ipv6=False, message='Invalid IP address')])
    submit = SubmitField('Ver')