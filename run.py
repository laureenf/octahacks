from datetime import datetime
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    place_found = db.Column(db.String(50), nullable=False)
    date_found = db.Column(db.DateTime, default=datetime.utcnow)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    station = db.relationship('Station')

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contact_no = db.Column(db.String(10), unique=True, nullable=False)

class Police(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    station = db.relationship('Station')


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/login')
def login():
    return 'Login'

@app.route('/register')
def register():
    return 'Register'

if __name__ == '__main__':
    app.run(debug=True)