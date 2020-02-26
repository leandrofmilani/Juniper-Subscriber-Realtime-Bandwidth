# Juniper-Subscriber-Realtime-Bandwidth
Web interface to visualize the real-time bandwidth utilization of a subscriber PPPoE in Juniper (Junos) devices

### How To Use
1. Install Python3.6 or higher
1. Install python3-venv
1. Clone repo
1. Create a virtual environment
    1. cd /path/to/repo
    1. python3 -m venv env
    1. source env/bin/activate
1. Install requirements: 
    1. pip install -r requirements.txt 
1. Edit the file JuniperBandwidth/login_juniper.json and change to your Juniper login and password.
1. Run: python3 run.py

The Juniper user needs at least have a user with permission of the class read-only and must also have the services netconf and ssh enabled.

Juniper commands:
```
set system login user username class read-only
set system login user username authentication plain-text-password password
set system services netconf ssh
```

You can use Nginx as a proxy to have web access to the application in production. Following this tutorial:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

Here my configs for production:

###### wsgi.py
```
from JuniperBandwidth import app

if __name__ == '__main__':
    app.run()
```

###### juniperbandwidth.ini
```
[uwsgi]
req-logger = file:/var/log/juniperbandwidth/access.log
logger = file:/var/log/juniperbandwidth/error.log

module = wsgi:app

master = true
processes = 5

die-on-term = true

http = :5000
```

###### /etc/systemd/system/juniperbandwidth.service 
```
[Unit]
Description=uWSGI instance to serve juniperbandwidth
After=network.target

[Service]
User=administrador
Group=www-data
WorkingDirectory=/opt/Juniper-Subscriber-Realtime-Bandwidth
Environment="PATH=/opt/Juniper-Subscriber-Realtime-Bandwidth/env/bin"
ExecStart=/opt/Juniper-Subscriber-Realtime-Bandwidth/env/bin/uwsgi --ini juniperbandwidth.ini

[Install]
WantedBy=multi-user.target
```

###### /etc/nginx/sites-enabled/juniperbandwidth 
```
server {
    listen 81;
    server_name 10.0.2.15;

    location / {
	proxy_pass http://localhost:5000;
	proxy_buffering off;
    }
}
```

#### Initial Screen
![Initial_Screen](image_example1.jpeg?raw=true "Initial")

#### Chart Screen
![Chart_Screen](image_example2.jpeg?raw=true "Chart")
