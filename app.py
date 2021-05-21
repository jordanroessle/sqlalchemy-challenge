# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database set-up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# References to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# ['measurement.id', 'measurement.station', 'measurement.date', 'measurement.prcp', 'measurement.tobs']
# ['station.id', 'station.station', 'station.name', 'station.latitude', 'station.longitude', 'station.elevation']

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
		f"/api/v1.0/start_date<br>"
		f"/api/v1.0/start_date/end_date<br>"
		)


@app.route("/api/v1.0/precipitation")
def precipitation():
	# Open Session
	session = Session(engine)

	# Query date and prcp
	query = session.query(Measurement.date, Measurement.prcp).all()
	
	# Close Session
	session.close()

	return_dict = {}
	for result in query:
		return_dict[result[0]] = result[1]

	return(jsonify(return_dict))


@app.route("/api/v1.0/stations")
def stations():
	# Open Session
	session = Session(engine)

	# Query station names
	stations = session.query(Station.station, Station.name).all()
	
	# Close Session
	session.close()

	return(jsonify(stations))

@app.route("/api/v1.0/tobs")
def tobs():
	# Open Session
	session = Session(engine)

	# Date set-up
	recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

	# Change to datetime object
	split = recent_date[0].split('-')
	recent_date = dt.date(int(split[0]), int(split[1]), int(split[2]))

	# Calculate one year before most recent data point
	year_ago = recent_date - dt.timedelta(days=365)

	# Find most active station
	most_active = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

	# Find most active station's temperature in the last year
	temperature_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.station == most_active).all()

	# Close session
	session.close()
	return(jsonify(temperature_year))

@app.route("/api/v1.0/<start>")
def start(start):
	# Open Session
	session = Session(engine)

	split = start.split('-')
	try: 
		start_date = dt.date(int(split[0]), int(split[1]), int(split[2]))
	except:
		return("The date you entered is invalid. Please try again while following this format: YYYY-MM-DD")

	temperatures = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start_date).all()
	
	# Close Session
	session.close()

	return(jsonify(temperatures))

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
	# Open Session
	session = Session(engine)

	split = start.split('-')
	try: 
		start_date = dt.date(int(split[0]), int(split[1]), int(split[2]))
	except:
		return("The FIRST date you entered is invalid. Please try again while following this format: YYYY-MM-DD")

	split = end.split('-')
	try: 
		end_date = dt.date(int(split[0]), int(split[1]), int(split[2]))
	except:
		return("The SECOND date you entered is invalid. Please try again while following this format: YYYY-MM-DD")

	temperatures = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
	
	# Close Session
	session.close()
	
	return(jsonify(temperatures))

if __name__ == '__main__':
	app.run(debug=True)