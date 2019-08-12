from flask import Flask, render_template, Response, url_for, flash, redirect, session
from forms import UsernameForm
from sse import ServerSentEvent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdbyegf2yveuyvdfstdf1twe51d5dfdfst'

###USAR git hub - ver questao das senhas nos arquivos aqui do codigo

#ver https://nagix.github.io/chartjs-plugin-streaming/samples/line-horizontal.html
#ou https://redstapler.co/javascript-realtime-chart-plotly/
# ~/Downloads/zingchart-branded-version.zip

@app.route('/', methods=['GET', 'POST'])
def index():
	form = UsernameForm()
	if form.validate_on_submit():
		session['username'] = form.username.data
		session['ip'] = form.ip.data
		# if (form.username.data != 'loja.cco'):
		# 	flash(f"Username {form.username.data} not found!","danger")
		# else:
		return redirect(url_for('realtime'))
	return render_template('index.html', title='Home', form=form)

@app.route('/realtime')
def realtime():
	return render_template('ploty.html', title='Realtime')

@app.route('/data')
def data():
	username = session.get('username', None)
	ip = session.get('ip', None)
	sse = ServerSentEvent(username, ip)
	generate = sse.generate()
	return Response(generate, mimetype= 'text/event-stream')

if __name__ == "__main__":
	app.run(debug=True)