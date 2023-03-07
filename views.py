from flasgger.utils import swag_from
from flask import request, make_response, abort
from flask.blueprints import Blueprint
from models import db, Weather, WeatherStats
from utils import AlchemyEncoder
import dask.dataframe as dd
import json
import os
import sqlite3

weather = Blueprint(
    'weather',
    __name__,
)


@swag_from("apidocs/weather_ingest.yml")
@weather.route('/api/weather/ingest')
def ingest_weather_data():
    ''' Ingest API for weather data.'''
    # list to store Dask dataframes for each file
    dataframes = []
    directory = "wx_data"
    if request.args.get('dir'):
        directory = request.args.get('dir')
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return abort(
            make_response(json.dumps({"message":
                                      "Directory does not exist."})))
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)

            # create Dask dataframe from text file
            dataframe = dd.read_csv(
                filepath,
                sep="\t",
                header=None,
                names=["date", "max_temp", "min_temp", "precipitation"])

            # add filename as new column
            dataframe["station_id"] = filename[:11]
            dataframes.append(dataframe)

    # concatenate Dask dataframes into one
    dataframe = dd.concat(dataframes)

    # compute the final dataframe and convert to Pandas dataframe
    dataframe = dataframe.compute()
    dataframe = dataframe.reset_index(drop=True)

    #Drop the -9999 indicating the empty values
    stats = dataframe[(dataframe['max_temp'] != -9999) |
                      (dataframe['min_temp'] != -9999) |
                      (dataframe['precipitation'] != -9999)]

    #creating the stats data
    stats = stats.groupby(['station_id',
                           dataframe['date'].map(str).str[:4]]).agg({
                               'max_temp':
                               'mean',
                               'min_temp':
                               'mean',
                               'precipitation':
                               'sum'
                           }).reset_index()

    stats.rename(columns={
        'max_temp': 'avg_max_temp',
        'min_temp': 'avg_min_temp',
        'precipitation': 'total_acc_precipitation'
    },
                 inplace=True)

    conn = sqlite3.connect('instance/database.db')

    # write data to database
    dataframe.to_sql("weather",
                     conn,
                     if_exists="replace",
                     index=True,
                     index_label='id')
    stats.to_sql("weather_stats",
                 conn,
                 if_exists="replace",
                 index=True,
                 index_label='id')
    # close database connection
    conn.close()
    r = make_response(json.dumps({"message": "Data Ingested."}))
    r.headers['Content-Type'] = 'application/json'
    r.mimetype = 'application/json'
    return r


@swag_from("apidocs/weather_data.yml")
@weather.route('/api/weather')
def get_all_weather_data():
    ''' Get all weather data.'''
    weather_data = Weather.query
    if request.args.get('station_id'):
        weather_data = weather_data.filter_by(
            station_id=request.args.get('station_id'))
    if request.args.get('date'):
        weather_data = weather_data.filter_by(date=request.args.get('date'))
    total = weather_data.count()
    limit = 500
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
        if limit > 500:
            limit = 500
    weather_data = weather_data.limit(limit)
    if request.args.get('offset'):
        offset = int(request.args.get('offset'))
        weather_data = weather_data.offset(offset)
    weather_data = weather_data.all()
    r = make_response(
        json.dumps({
            "data": weather_data,
            "count": total
        }, cls=AlchemyEncoder))
    r.headers['Content-Type'] = 'application/json'
    r.mimetype = 'application/json'
    return r


@swag_from("apidocs/weather_stats.yml")
@weather.route('/api/weather/stats')
def get_all_weather_stats_data():
    ''' Get all weather stats data.'''
    weather_data = WeatherStats.query
    if request.args.get('station_id'):
        weather_data = weather_data.filter_by(
            station_id=request.args.get('station_id'))
    total = weather_data.count()
    limit = 500
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
        if limit > 500:
            limit = 500
    weather_data = weather_data.limit(limit)
    if request.args.get('offset'):
        offset = int(request.args.get('offset'))
        weather_data = weather_data.offset(offset)
    weather_data = weather_data.all()
    r = make_response(
        json.dumps({
            "data": weather_data,
            "count": total
        }, cls=AlchemyEncoder))
    r.headers['Content-Type'] = 'application/json'
    r.mimetype = 'application/json'
    return r
