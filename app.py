# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database set-up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# References to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
	# Print all api routes
	return (
		f"Availble Routes:<br>" 
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/<start><br>"
		f"/api/v1.0/<start>/<end><br>"
		)


@app.route("/api/v1.0/precipitation")
def precipitation():
 	return("precipitation")


@app.route("/api/v1.0/stations")
def stations():
 	return("stations")

@app.route("/api/v1.0/tobs")
def tobs():
 	return("tobs")

@app.route("/api/v1.0/<start>")
def start(start):
 	return("start")

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
 	return("start end")

if __name__ == '__main__':
	app.run(debug=True)