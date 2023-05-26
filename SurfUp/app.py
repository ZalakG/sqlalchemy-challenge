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
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
    )
    return routes

# Return json precipitation
@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value."""
    data_prcp_score = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all() ## this query is performed in the climate_starter.ipynb to get the results
    
    session.close()
    
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
    session = Session(engine)
    ### Query all stations ###
    station = session.query(Station.station, Station.name).all()

    session.close()

    ### Convert list of tuples into normal list ###
    all_station = list(np.ravel(station))   
    
    return jsonify(all_station)

# Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    yearago_date = dt.date(2017,8,23) - dt.timedelta( days = 365)

    last_12months_temp_result = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= yearago_date).all()
    
    session.close()

    tobs = list(np.ravel(last_12months_temp_result))

        ### Return jsonified data for the last year of data ###
    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature 
# for a specified start or start-end range.

@app.route("/api/v1.0/<start>", defaults = {"end" : None})
@app.route("/api/v1.0/<start>/<end>")



def temptatus(start, end ):

    session = Session(engine)

    status = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    
    ### If we have bot ha start date and end date
    if end != None:
        status_result = session.query(*status).filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).all()
        temp = list(np.ravel(status_result))

    else:
        
        status_result = session.query(*status).filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).all()
    
    session.close()

    ## convert Query status_result into  list  ###

    temp_list = []
    temp_data = False
    for min_temp, avg_temp, max_temp in temp_data:
        if min_temp == None or avg_temp == None or max_temp == None:
            temp_data = True
        temp_list.append(min_temp)
        temp_list.append(avg_temp)
        temp_list.append(max_temp)

        ### Return JSON dictionary of temp_data ###

    if temp_data == True:

        return f"No Data found for given date."
    
    else:

        return jsonify(temp_list)     
    

    
    
if __name__ == '__main__':
    app.run()