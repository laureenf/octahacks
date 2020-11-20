from datetime import datetime
from flask import Flask,redirect,render_template,url_for
from flask_login import UserMixin,LoginManager,login_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
  return Police.get(user_id)

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
    password_hash = db.Column(db.String(60), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    station = db.relationship('Station')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
         return True if self.password_hash==password else False


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/login', methods=['GET','POST'])
def login():
  render_template('base.html',current_user=None)
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    # query User here:
    user = Police.query.filter_by(email=form.email.data).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.password.data):
      # login user here:
      login_user(user, remember=form.remember.data)
      render_template('base.html',current_user=user)
      next_page = url_for('index')
      return redirect(next_page)
    else:
      return redirect(url_for('login',_external=True))
  return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(csrf_enabled=False)
  if form.validate_on_submit():
    user = Police(email=form.email.data, name=form.name.data, station=form.station.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
  return render_template('register.html', title='Register', form=form) 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))   


class RegistrationForm(FlaskForm):
  name=StringField('Name', validators=[DataRequired()])
  number=IntegerField('Number', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  station = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')    

class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')    

if __name__ == '__main__':
    app.run(debug=True)


