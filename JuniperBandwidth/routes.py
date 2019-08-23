from flask import render_template, Response, url_for, flash, redirect, session
from JuniperBandwidth import app
from JuniperBandwidth.forms import UsernameForm
from JuniperBandwidth.sse import ServerSentEvent

@app.route('/', methods=['GET', 'POST'])
def index():
	form = UsernameForm()
	if form.validate_on_submit():
		session['username'] = form.username.data
		session['ip'] = form.ip.data
		return redirect(url_for('realtime'))
	return render_template('index.html', title='JuniperBandwidth', form=form)

@app.route('/realtime')
def realtime():
	return render_template('realtime.html', title='Realtime')

@app.route('/data')
def data():
	username = session.get('username', None)
	ip = session.get('ip', None)
	sse = ServerSentEvent(username, ip)
	generate = sse.generate()
	return Response(generate, mimetype= 'text/event-stream')

if __name__ == "__main__":
	app.run()