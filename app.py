from flask import Flask, render_template, request, jsonify, redirect, flash
import sqlite3
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
db = sqlite3.connect('sitenames.db')
cursor = db.cursor()
print(cursor.execute("SELECT * FROM sites LIMIT 5;").fetchall())
db.close()


@app.route('/')
def index():
    townresults = getSiteList()
    return render_template("index.html", townresults=townresults)


@app.route('/weather', methods=['GET'])
def weather():
    townresults = getSiteList()
    town = request.args.get("townsearch")
    db = sqlite3.connect('sitenames.db')
    cursor = db.cursor()
    query = cursor.execute("SELECT name, codes, pcodes FROM sites WHERE name IS :name", {
        'name': town})
    results = query.fetchall()
    if not results:
        flash('Town Not Found')
        return redirect("/")
    for result in results:
        if town not in result:
            flash('Town Not Found')
            return redirect("/")

    site = results[0][1]
    pcode = results[0][2]
    URL = f'https://dd.weather.gc.ca/citypage_weather/xml/{pcode}/{site}_e.xml'
    response = requests.get(URL)

    weather = get_weather(response)
    hourly = get_hourly_forecast(response)
    almanac = get_almanac(response)
    return render_template("weather.html", weather=weather, almanac=almanac, hourly=hourly, townresults=townresults)


# @app.route("/search", methods=["GET"])
# def search():
#     # Get the input value from the request
#     db = sqlite3.connect('sitenames.db')
#     cursor = db.cursor()
#     inputValue = request.args.get("input")
#     if inputValue:
#         query = cursor.execute('SELECT codes, name, pcodes FROM sites WHERE name LIKE :name', {
#                                'name': '%' + inputValue + '%'})
#         results = query.fetchall()
#     else:
#         results = []
#     db.close()
#     return jsonify(results)


# @app.route('/geolocationdata', methods=['GET'])
# def geolocationdata():
#     print("GETTING DATS THIS PART IS WORKING?")
#     if 'latitude' in request.args and 'longitude' in request.args:
#         print("Hello")
#         site = sitegetter(
#             lat=request.args['latitude'], long=request.args['longitude'])

#         if site != 'none':
#             return 'success', 200, {'Content-Type': 'text/plain'}
#         else:
#             return 'lat and long not found', 400, {'Content-Type': 'text/plain'}
#     else:
#         return "what the hell is going on"


def get_weather(response):

    # create an xml element tree
    root = ET.fromstring(response.content)

    # get the current conditions element
    current_conditions = root.find('currentConditions')

    # get the hourly forecast
    # get the AST dateTime element
    # ast_date_time = root.find(".//dateTime[@name='observation'][@zone='UTC']")

    # get all the data
    temperature = current_conditions.find('temperature').text
    station = current_conditions.find('station').text
    wind_speed = current_conditions.find('wind/speed').text
    wind_direction = current_conditions.find('wind/direction').text
    wind_bearing = current_conditions.find('wind/bearing').text
    condition = current_conditions.find('condition').text
    iconcode = current_conditions.find('iconCode').text
    textsummary = current_conditions.find('dateTime/timeStamp').text
    date_string = textsummary
    date_time_obj = datetime.strptime(date_string, '%Y%m%d%H%M%S')
    print(date_time_obj)

    dewpoint = current_conditions.find('dewpoint').text
    pressure = current_conditions.find('pressure').text
    visibility = current_conditions.find('visibility').text
    relative_humidity = current_conditions.find('relativeHumidity').text

    date_time_12hr = date_time_obj.strftime('%Y %m %d %H %M %S')
    textsummary = date_time_12hr

    # return the data as a dict
    return {'temperature': temperature, 'wind_speed': wind_speed, 'wind_direction': wind_direction, 'wind_bearing': wind_bearing, 'condition': condition, 'iconcode': iconcode, 'textsummary': textsummary, 'station': station, 'dewpoint': dewpoint, 'pressure': pressure, 'visibility': visibility, 'relative_humidity': relative_humidity}


def get_hourly_forecast(response):
    root = ET.fromstring(response.content)
    hourlyForecastGroup = root.find('hourlyForecastGroup')

    # create empty dictionary
    forecast_weather = {}

    # loop through each hourly forecast
    for hourlyForecast in hourlyForecastGroup.findall('hourlyForecast'):
        # grab dateTimeUTC, condition, iconCode, temperature, windChill, wind speed, wind direction, and wind gusting
        dateTimeUTC = hourlyForecast.get('dateTimeUTC')
        condition = hourlyForecast.find('condition').text
        iconCode = hourlyForecast.find('iconCode').text
        temperature = hourlyForecast.find('temperature').text
        windChill = hourlyForecast.find('windChill')
        windSpeed = hourlyForecast.find('wind/speed').text
        windDirFull = hourlyForecast.find('wind/direction').get('windDirFull')
        windGusting = hourlyForecast.find('wind/gust').text

        # convert dateTimeUTC to AST
        date_time_utc = datetime.strptime(dateTimeUTC, '%Y%m%d%H%M')

        # add data to dictionary
        forecast_weather[date_time_utc.strftime('%Y%m%d%H%M')] = {
            'forecast_time': date_time_utc.strftime('%Y %m %d %H %M %S'),
            'condition': condition,
            'iconCode': iconCode,
            'temperature': temperature,
            'windChill': windChill.text if windChill is not None else None,
            'windSpeed': windSpeed,
            'windDirFull': windDirFull,
            'windGusting': windGusting
        }
    # return forecast weather
    return forecast_weather


def get_almanac(response):
    # create an xml element tree
    root = ET.fromstring(response.content)

    # get all the data
    almanac = root.find('almanac')
    extremeMaxTemp = almanac.find('temperature[@class="extremeMax"]').text
    extremeMax_year = almanac.find(
        'temperature[@class="extremeMax"]').get('year')
    extremeMinTemp = almanac.find('temperature[@class="extremeMin"]').text
    extremeMin_year = almanac.find(
        'temperature[@class="extremeMin"]').get('year')
    normalMaxTemp = almanac.find('temperature[@class="normalMax"]').text
    normalMax_year = almanac.find(
        'temperature[@class="normalMax"]').get('year')
    normalMinTemp = almanac.find('temperature[@class="normalMin"]').text
    normalMin_year = almanac.find(
        'temperature[@class="normalMin"]').get('year')
    normalMeanTemp = almanac.find('temperature[@class="normalMean"]').text
    normalMean_year = almanac.find(
        'temperature[@class="normalMean"]').get('year')
    extremeRainfall = almanac.find(
        'precipitation[@class="extremeRainfall"]').text
    extremeRainfall_year = almanac.find(
        'precipitation[@class="extremeRainfall"]').get('year')
    extremeSnowfall = almanac.find(
        'precipitation[@class="extremeSnowfall"]').text
    extremeSnowfall_year = almanac.find(
        'precipitation[@class="extremeSnowfall"]').get('year')
    extremePrecipitation = almanac.find(
        'precipitation[@class="extremePrecipitation"]').text
    extremePrecipitation_year = almanac.find(
        'precipitation[@class="extremePrecipitation"]').get('year')
    extremeSnowOnGround = almanac.find(
        'precipitation[@class="extremeSnowOnGround"]').text
    extremeSnowOnGround_year = almanac.find(
        'precipitation[@class="extremeSnowOnGround"]').get('year')
    almanacpop = almanac.find('pop').text
    # return the data as a dict
    return {'extremeMaxTemp': extremeMaxTemp, 'extremeMax_year': extremeMax_year, 'extremeMinTemp': extremeMinTemp, 'extremeMin_year': extremeMin_year, 'normalMaxTemp': normalMaxTemp, 'normalMax_year': normalMax_year, 'normalMinTemp': normalMinTemp, 'normalMin_year': normalMin_year, 'normalMeanTemp': normalMeanTemp, 'normalMean_year': normalMean_year, 'extremeRainfall': extremeRainfall, 'extremeRainfall_year': extremeRainfall_year, 'extremeSnowfall': extremeSnowfall, 'extremeSnowfall_year': extremeSnowfall_year, 'extremePrecipitation': extremePrecipitation, 'extremePrecipitation_year': extremePrecipitation_year, 'extremeSnowOnGround': extremeSnowOnGround, 'extremeSnowOnGround_year': extremeSnowOnGround_year, 'almanacpop': almanacpop}


def getSiteList():
    db = sqlite3.connect('sitenames.db')
    cursor = db.cursor()
    query = cursor.execute("SELECT name FROM sites")
    results = query.fetchall()
    townresults = []
    for result in results:
        town = result[0]
        townresults.append(town)

    return townresults


if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
