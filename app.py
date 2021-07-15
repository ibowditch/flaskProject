from flask import Flask, render_template, request
import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, String, Float, DateTime, desc
import dateutil.parser

import logging
# logger = logging.getLogger(__name__)


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')


# from systemd import journal       #TODO can't get to install systemd in this project somehow
import logging.handlers
# Log all messages to the system journal
# loghandler = JournalHandler(SYSLOG_IDENTIFIER=SYSLOG_ID)
# logger = logging.getLogger(SYSLOG_ID)
# logger.addHandler(loghandler)
# logger.setLevel(logging.DEBUG)  # TODO change to INFO in production

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

######### Models #########

class Weather(db.Model):
    id =        sa.Column(Integer,  primary_key=True)
    ts =        sa.Column(DateTime, unique=False)
    temp =      sa.Column(Float,    unique=False)
    rh =        sa.Column(Float,    unique=False)
    wind_dird = sa.Column(Integer,  unique=False)               # Wind direction in degrees
    wind_dirc = sa.Column(Text,     unique=False)               # Win direction as compass reading
    wind_sp =   sa.Column(Float,    unique=False)               # in km/h

    def __repr__(self):
        return f'Weather at {self.ts}: Temp={self.temp} RH={self.rh} wind={self.wind_sp} dir={self.wind_dirc}'


db.create_all()

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/latest')
def latest():
    lastrep = Weather.query.order_by(desc(Weather.ts)).first()           # No last() available, so get latest
    return render_template('bsstationj.html', rep=lastrep)

@app.route('/update', methods=['GET', 'POST'])
def update():
    neww = Weather(ts=dateutil.parser.parse(request.values['timestamp']),
                   temp=float(request.values['temp_c']),
                   rh=float(request.values['relative_humidity']),
                   wind_dird=int(request.values['wind_degrees']),
                   wind_dirc=degToCompass(int(request.values['wind_degrees'])),
                   wind_sp=float(request.values['wind_mph'])*1.60934)                   # Convert mph -> kph
    db.session.add(neww)
    db.session.commit()
    # logging.info(neww)
    print(neww)
    return 'update'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

