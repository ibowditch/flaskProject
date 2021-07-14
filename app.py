from flask import Flask, render_template, request
import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Float, DateTime
import dateutil.parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

######### Models #########

class Weather(db.Model):
    id =    sa.Column(Integer, primary_key=True)
    ts =    sa.Column(DateTime, unique=False)
    temp =  sa.Column(Float, unique=False)
    rh =    sa.Column(Float, unique=False)

    def __repr__(self):
        return 'ts %s' % self.ts

db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/cakes')
# def cakes():
#     return 'Yummy cakes!'
#
# @app.route('/hello/<name>')
# def hello(name):
#     return render_template('page.html', name=name)

@app.route('/update', methods=['GET', 'POST'])
def update():
    r = request
    neww = Weather(ts=dateutil.parser.parse(r.values['timestamp']), temp=float(r.values['temp_c']), rh=float(r.values['relative_humidity']))
    db.session.add(neww)
    db.session.commit()
    allw = Weather.query.all()
    return 'update'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

