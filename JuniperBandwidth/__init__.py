from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdbyegf2yveuyvdfstdf1twe51d5dfdfst'

from JuniperBandwidth import routes