from flask import Flask, render_template, request
import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, String, Float, DateTime, desc
import dateutil.parser
import numpy as np
from sklearn.linear_model import LinearRegression

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
db.create_all()

######### Models #########

class Weather(db.Model):
    id =        sa.Column(Integer,  primary_key=True)
    ts =        sa.Column(DateTime, unique=False)               # Timestamp of record
    temp =      sa.Column(Float,    unique=False)               # Temperature in degrees centigrade
    rh =        sa.Column(Float,    unique=False)               # Relative humidity
    wind_dird = sa.Column(Integer,  unique=False)               # Wind direction in degrees
    wind_sp =   sa.Column(Float,    unique=False)               # Win speed in km/h

    @property
    def wind_cardinal(self):                                    # Show wind direction as cardinal (eg. WNW)
        return degToCardinal(self.wind_dird)

    def __repr__(self):
        return f'Weather at {self.ts}: Temp={self.temp} RH={self.rh} wind={self.wind_sp} dir={self.wind_cardinal}'

## Utilities

def degToCardinal(degrees):
    compass_points = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    index = int((degrees/(360.0/len(compass_points)))+.5) % len(compass_points)
    return compass_points[index]

def trend_slope(x_readings, y_readings):
    x = np.array(x_readings).reshape((-1, 1))
    y = np.array(y_readings)
    model = LinearRegression().fit(x, y)
    return model.coef_

## Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/latest')
def latest():
    lastrep = Weather.query.order_by(desc(Weather.ts)).first()           # No last() available, so get latest
    return render_template('bsstationj.html', rep=lastrep)

@app.route('/latest5')
def latest5():
    lastrep = Weather.query.order_by(Weather.ts).all()[:5]         # Last 5 readings

    last_times = [(lastrep[i].ts-lastrep[0].ts).total_seconds() for i in range(len(lastrep))]
    last_tmps =  [ls.temp    for ls in lastrep]
    last_rhs =   [ls.rh      for ls in lastrep]
    last_winds = [ls.wind_sp for ls in lastrep]

    tmp_slope =  trend_slope(last_times, last_tmps)
    rh_slope =   trend_slope(last_times, last_rhs)
    wind_slope = trend_slope(last_times, last_winds)
    return 'latest5'


@app.route('/update', methods=['GET', 'POST'])
def update():
    neww = Weather(ts =         dateutil.parser.parse(request.values['timestamp']),
                   temp =       float(request.values['temp_c']),
                   rh =         float(request.values['relative_humidity']),
                   wind_dird =  int(request.values['wind_degrees']),
                   wind_sp =    float(request.values['wind_mph'])*1.60934)                   # Convert mph -> kph
    db.session.add(neww)
    db.session.commit()
    # logging.info(neww)
    print(neww)
    return 'update'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

