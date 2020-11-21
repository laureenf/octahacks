from datetime import datetime
from flask import Flask,redirect,render_template,url_for, request
from flask_login import UserMixin,LoginManager,login_user,logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYSECRETKEY123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
  return Station.query.filter_by(id=user_id).first()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    place_found = db.Column(db.String(50), nullable=False)
    date_found = db.Column(db.String(10), nullable=False)

    station_id = db.Column(db.Integer, db.ForeignKey('station.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    station = db.relationship('Station')

class Station(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contact_no = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Station {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
         return True if self.password_hash == password else False

db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    # query User here:
    form = request.form
    user = Station.query.filter_by(email=form.get('mailid')).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.get('pass')):
      # login user here:
      login_user(user)
      render_template('enteritem.html')
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('enteritem'))
    else:
      return redirect(url_for('login', _external=True))
  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    # query User here:
    form = request.form
    if form.get('pass') == form.get('pass2'):
      user = Station(email=form.get('mailid'), name=form.get('stationname'), contact_no=form.get('number'), address=form.get('address'))
      user.set_password(form.get('pass'))
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('login'))
  return render_template('register.html', title='Register') 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/enteritem", methods=['GET', 'POST'])
@login_required
def enteritem():
  if request.method == 'POST':
    form = request.form
    item = Item(place_found=form.get('place_found'), station_id=current_user.id, name=form.get('Item_name'), date_found=str(form.get('Date_found')), description=form.get('desc'))
    db.session.add(item)
    db.session.commit()
  return render_template('enteritem.html')

@app.route("/itemview")
def itemview():
  items = Item.query.all()
  search = request.args.get('search')
  items = Item.query.filter_by(name=search)
  return render_template('itemview.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)


