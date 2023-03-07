from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class Weather(db.Model):
    ''' Weather Model'''
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(8), nullable=False)
    max_temp = db.Column(db.Integer, nullable=True)
    min_temp = db.Column(db.Integer, nullable=True)
    precipitation = db.Column(db.Integer, nullable=True)
    station_id = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f'<Weather {self.station_id}>'


class WeatherStats(db.Model):
    ''' WeatherStats Model'''
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(12), nullable=False)
    avg_max_temp = db.Column(db.Integer, nullable=True)
    avg_min_temp = db.Column(db.Integer, nullable=True)
    total_acc_precipitation = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<WeatherStats {self.station_id}>'