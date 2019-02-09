import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, )
    rights = db.Column(db.Integer, nullable=False, default=0)
    password_hash = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Presence(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	enter = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	exit = db.Column(db.DateTime, default=None)
	user = db.relationship("User")

	def set_date(self):
		self.exit = datetime.datetime.utcnow
