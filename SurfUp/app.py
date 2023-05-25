# Import the dependencies.
from flask import Flask, jsonify 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)


# Save references to each table
Measurement  = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def Welcome():
    """Save all the available route in a variable"""
    routes = (
        f'Wlcome to the SQL-Alchemy API!<br/><br/>'
        f'Following are the available API routes<br/><br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/[start_date/end_date<br/>'
    )
    return routes

# Return json precipitation
@app.route("/api/v1.0/precipitation")
def percipitation():
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value."""
    data_prcp_score = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all() ## this query is performed in the climate_starter.ipynb to get the results
    
    ### Create a dictionary from the row data and append to a list of percipitation
    percipitation = [] ## create variable that holds the list 
    for date, prcp in data_prcp_score:
        prcp_dict = {}  
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        percipitation.append(prcp_dict)
    return jsonify(percipitation) ## Returns the JSON representation of  dictionary.

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    ### Query all stations ###
    station = session.query(Station.station, Station.name).all()

    ### Convert list of tuples into normal list ###
    all_station = list(np.ravel(station))   
    
    return jsonify(all_station)

# Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    yearago_date = dt.date(2017,8,23) - dt.timedelta( days = 365)

    last_12months_temp_result = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= yearago_date).all()
    tobs = list(np.ravel(last_12months_temp_result))
        ### Return jsonified data for the last year of data ###
    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature 
# for a specified start or start-end range.

@app.route("/api/v1.0/start_date")
def start_date(start_date):





     
    
    
    
    
if __name__ == '__main__':
    app.run()