import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Stations= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"api/v1.0/&lt;start&gt;<br/>"
        f"api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"

        
    )

@app.route("/api/v1.0/precipitations")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return one year of precipitaion"""
    # Query max date
    max_date = session.query(func.max(Measurement.date)).first()

    """Return previous year of precipitaion"""
    previous_year= dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Return last 12 months of Measurement and Precipitaion"""
    last_12_months=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>previous_year).all()

    session.close()

    precipitation_data = {date: prcp for date, prcp in last_12_months}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations_number():
    session= Session(engine)
    number_of_stations=session.query(Stations.station).all()
    stations_result=[]
    for number_of_station in number_of_stations:
        stations_result.append(number_of_station[0])
    session.close()
    return jsonify(stations_result)


@app.route("/api/v1.0/tobs")
def tobs ():
    session= Session(engine)
    previous_year=dt.date(2017, 8 ,23)- dt.timedelta(days=365)
    stations_lists=session.query(Measurement.tobs).filter(Measurement.date>=previous_year).filter(Measurement.station=='USC00519281').all()
    station_list_result=[]
    for station_list in stations_lists:
        station_list_result.append(station_list[0])
    session.close()
    return jsonify(station_list_result)

@app.route("/api/v1.0/<start>")
def start(start):
    session= Session(engine)
    min_max_avg=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    session.close()
    min_max_avg_result=[]
    min_max_avg_result.append(min_max_avg[0][0])
    min_max_avg_result.append(min_max_avg[0][1])
    min_max_avg_result.append(min_max_avg[0][2])
    return jsonify(min_max_avg_result)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session= Session(engine)
    min_max_avg=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()
    min_max_avg_result=[]
    min_max_avg_result.append(min_max_avg[0][0])
    min_max_avg_result.append(min_max_avg[0][1])
    min_max_avg_result.append(min_max_avg[0][2])
    return jsonify(min_max_avg_result)

    
if __name__ == '__main__':
    app.run()

