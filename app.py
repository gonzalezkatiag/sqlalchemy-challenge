# Import dependencies
from types import prepare_class
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station=Base.classes.station

session = Session(engine)

# Create Flask 
app = Flask(__name__)


# Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App! C<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start/<start> <br/>"
        f"/api/v1.0/start-end/<start>/<end> <br/>"
    )

# Precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Session link
    session = Session(engine)
    # Query 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

# Stations  
@app.route("/api/v1.0/stations")
def stations():
    # Session link
    session = Session(engine)
    # Query
    results = session.query(Station.station, Station.name).all()
    session.close()

    stations_all = list(np.ravel(results))
    return jsonify(stations_all)

#TOBS for most active station "USC00519281"
@app.route("/api/v1.0/tobs")
def tobs():
    # Session link
    session = Session(engine)
    # Query
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date > "2016-08-18").all()
    all_tobs = list(np.ravel(results))

    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    session.close()

    return jsonify(all_tobs)


@app.route("/api/v1.0/start/<start>")
def start_date(start):
    session = Session(engine)

    sel = [Measurement.date, 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.min(Measurement.tobs)]
    results = session.query(*sel).\
        filter(Measurement.date >=start).all()
        
    session.close()

    all_data = []
    for x in results:
        all_data.append({'date': x[0],'avg tobs': x[1],'max tobs': x[2],'min tobs': x[3]})

    return jsonify(all_data)

@app.route("/api/v1.0/start-end/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    sel = [Measurement.date, 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.min(Measurement.tobs)]
    results = session.query(*sel).\
        filter(Measurement.date >=start).filter(Measurement.date <=end).all()
        
    session.close()

    all_data = []
    for x in results:
        all_data.append({'date': x[0],'avg tobs': x[1],'max tobs': x[2],'min tobs': x[3]})

    return jsonify(all_data)

if __name__ == "__main__":
    app.run(debug=True)