from flask import Flask, render_template, request
import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy import Column, Integer, Text, Float, DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

######### Models #########
class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True
    pass

######## Initialize ########
BaseModel.set_session(db.session)

class Weather(BaseModel):
    id = sa.Column(Integer, primary_key=True)
    ts = sa.Column(DateTime, unique=False)
    temp = sa.Column(Float, unique=False)
    rh = sa.Column(Float, unique=False)

db.create_all()


@app.route('/')
def index():
    # return 'Hello World!'
    return render_template('index.html')

@app.route('/cakes')
def cakes():
    neww = Weather.create(ts=datetime.datetime.now(), temp=10.5, rh=65.0)
    return 'Yummy cakes!'

@app.route('/hello/<name>')
def hello(name):
    r = request
    return render_template('page.html', name=name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
