from flask import Flask, request, render_template, Response, redirect, url_for, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import random
from flask import jsonify
from sqlalchemy.orm import load_only
import datetime
import json
from serializer import *
import flask_login
import os
from flask_login import current_user, login_user, logout_user
import requests
import re
from PIL import Image
from io import StringIO
import base64
import io
import cv2
import numpy as np

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	DEBUG = True
	SECRET_KEY = 'W9xJeJKrUqiG9cONoM4O9ZtpZ1k4wrRJXexHtP8V'

	SENSORS_URL = 'http://10.14.194.162:5000/get_data'
	FACE_URL = 'http://10.14.131.236:5000/recognize'
	FINGER_PRINT_URL = 'http://10.14.167.219:5000/get_fingerprint'
	THERMOSTAT_URL = 'http://10.14.157.202:8888/get_regression'


app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
login = flask_login.LoginManager(app)
login_required = flask_login.login_required
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/<path:path>')
def static_file(path):
	return app.send_static_file(path)


from flask_wtf import FlaskForm


@app.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('home'))

	user = User.query.filter_by(name=request.form['username']).first()
	if user is None or not user.check_password(request.form['password']):

		flash('Invalid username or password')
		return redirect(url_for('login_page'))

	login_user(user, remember=True)

	return redirect(url_for('home'))


@app.route('/', methods=['GET'])
def login_page():

	if 'username' in session:
		return redirect(url_for('home'))

	return render_template('login.html')


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login_page'))


@app.route('/user/<user_id>')
@login_required
def user(user_id):
	user = User.query.filter_by(id=user_id).first_or_404()

	return render_template('user.html', data=user)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def home():
	# load_data()
	inhibitants = User.query.filter(User.rights.in_((2, 3)))
	friends = User.query.filter(User.rights.in_((0, 1)))
	data = {'users': inhibitants, 'friends': friends, 'sensors': get_data(Config.SENSORS_URL)}
	return render_template('index.html', data=data)


last_time_stamp = None
last_name = None
from datetime import datetime, timedelta

@app.route('/get_info', methods=['POST'])
@login_required
def get_info():
	sensors = get_data(Config.SENSORS_URL)

	finger_print = get_data(Config.FINGER_PRINT_URL)

	print(finger_print)

	if not finger_print:
		return jsonify(sensors)

	message = finger_print['Message1']

	if message == 'User not recognized':
		return jsonify(sensors)		
	
	name = message.split(' ')[0].lower()

	timestamp = datetime.fromtimestamp(finger_print['Timestamp1'])
	
	global last_time_stamp
	global last_name

	if last_time_stamp == timestamp:
		return jsonify(sensors)

	if last_name == name and \
		last_time_stamp + timedelta(seconds=5) > timestamp:

		last_time_stamp = timestamp
		return jsonify(sensors)

	last_name = name
	last_time_stamp = timestamp

	user = User.query.filter_by(name=name).first()

	if user is None or user.rights in (0, 1):
		sensors['fingerprint'] = [name, 0]
		return jsonify(sensors)

	sensors['fingerprint'] = [name, 1]
	return jsonify(sensors)


@app.route('/statistics', methods=['POST', 'GET'])
@login_required
def statistics():
	mes = db.session.query(Measurements).order_by(Measurements.id.desc()).limit(50).all()
	data = {'in': [], 'out': [], 'timestamps': [], 'humidity': []}

	for d in mes:
		data['in'].append(d.tIn)
		data['out'].append(d.tOut)
		data['timestamps'].append(d.date.strftime("%m-%d %H:%M"))
		data['humidity'].append(d.humidity)

	return render_template('statistics.html', data=data)


@app.route('/get_photo', methods=['POST'])
def get_photo():
	print('blabla')
	image_b64 = request.values['imgBase64']

	image_b64 = image_b64.replace('data:image/png;base64,', '')

	data = {'image': image_b64}
	# imgdata = base64.b64decode(str(image_b64))
	# image = Image.open(io.BytesIO(imgdata))
	# im = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
	# cv2.imwrite('data.png', im)
	answer = get_data(Config.FACE_URL, data)
	

	user = User.query.filter_by(name=answer['person']).first()
	if user is None:

		return redirect(url_for('login_page'))

	login_user(user, remember=True)
	return redirect(url_for('home'))


def get_data(url, data={}):
	try:
		r = requests.post(url, data=data, timeout=2)
		if r.status_code != 200:
			return {}
		return r.json()

	except:
		return {}


# import pandas as pd

# def load_data():
# 	m = Measurements.query.first()
# 	print(m.date)
# 	pass
# 	# df = pd.read_csv('static/data.csv', sep=',', header=0)

# 	# df['timestamp'] = df['timestamp'].apply(lambda x: (datetime.fromtimestamp(x)))

# 	# for col in ['tIn', 'tOut', 'humidity']:
# 	# 	df[col] = df[col].apply(lambda x: round(x, 2))

# 	# for index, row in df.iterrows():
# 	# 	m = Measurements(tIn=row.tIn, humidity=row.humidity, tOut=row.tOut)
# 	# 	db.session.add(m)

# 	# db.session.commit()

@app.before_first_request
def create_users():

	user = User.query.get(1)

	if user is not None:
		return

	users = [
		['maciek', 2],
		['patryk', 3],
		['wojtek', 2],
		['dawid', 3],
		['roman', 0],
		['stefan', 1],
		['ania', 0],
		['iza', 1]
	]

	for data in users:
		name, rights = data
		u = User(name=name, rights=rights)
		u.set_password('1234')
		db.session.add(u)

	db.session.commit()


if __name__ == '__main__':
	db.create_all()
	
	db.init_app(app)

	app.run(host='0.0.0.0', port=8000)