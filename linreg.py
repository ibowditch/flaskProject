import numpy as np
from sklearn.linear_model import LinearRegression

import datetime
from datetime import timedelta

dt1 = datetime.datetime(year=2021, month=7, day=16, hour=11, minute=30)
dtlist = [ dt1 + i*timedelta(minutes=5) for i in range(6) ]

xsecs = [ (dtlist[i] - dt1).total_seconds() for i in range(len(dtlist))]

temps_up = [ 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
temps_dn = [ 15.0, 14.0, 13.0, 12.0, 11.0, 10.0]
temps_fl = [ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0]

x = np.array(xsecs).reshape((-1, 1))
y = np.array(temps_fl)

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
r_inter = model.intercept_
r_slope = model.coef_

y = 10


