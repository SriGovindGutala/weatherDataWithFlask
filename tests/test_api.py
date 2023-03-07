import json
from app import create_app

app = create_app()


def test_weather_data():
    ''' Test weather data.'''
    response = app.test_client().get('/api/weather')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["data"]) == 500


def test_weather_stats_data():
    ''' Test weather stats data.'''
    response = app.test_client().get('/api/weather/stats')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["data"]) == 500
