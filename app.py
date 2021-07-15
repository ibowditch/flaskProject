from flask import Flask, render_template, request
import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Float, DateTime
import dateutil.parser

import logging
logger = logging.getLogger(__name__)

# from systemd import journal       #TODO can't get to install systemd in this project somehow
import logging.handlers
# Log all messages to the system journal
# loghandler = JournalHandler(SYSLOG_IDENTIFIER=SYSLOG_ID)
# logger = logging.getLogger(SYSLOG_ID)
# logger.addHandler(loghandler)
# logger.setLevel(logging.DEBUG)  # TODO change to INFO in production

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
        return f'Weather at {self.ts}: Temp={self.temp} RH={self.rh}'


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/latest')
def latest():
    lastrep = Weather.query.order_by(-Weather.ts).first()           # No last() available, so get latest
    return render_template('bsstationj.html', rep=lastrep)

@app.route('/update', methods=['GET', 'POST'])
def update():
    neww = Weather(ts=dateutil.parser.parse(request.values['timestamp']),
                   temp=float(request.values['temp_c']),
                   rh=float(request.values['relative_humidity']))
    db.session.add(neww)
    db.session.commit()
    logger.info(neww)
    return 'update'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

