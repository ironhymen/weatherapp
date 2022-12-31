from flask import Flask, render_template, request, jsonify, redirect, flash
import sqlite3
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
db = sqlite3.connect('sitenames.db')
cursor = db.cursor()
db.close()

# homepage route - displays a search bar and a list of towns to choose from in a dropdown menu
# if the user enters a town that is not in the database, they are redirected to the homepage with a flash message
# if the user enters a town that is in the database, they are redirected to the weather page


@app.route('/')
def index():
    # get the list of towns from the database
    townresults = getSiteList()
    # render the index.html template and pass the list of towns to the template
    return render_template("index.html", townresults=townresults)

# function to get the list of towns from the database


@app.route('/weather', methods=['GET'])
def weather():
    # get the list of towns from the database
    townresults = getSiteList()
    # get the town from the search bar
    town = request.args.get("townsearch")
    db = sqlite3.connect('sitenames.db')
    cursor = db.cursor()
    # query the database for the town
    query = cursor.execute("SELECT name, codes, pcodes FROM sites WHERE name IS :name", {
        'name': town})
    results = query.fetchall()
    # if the town is not in the database, redirect to the homepage with a flash message
    if not results:
        flash('Town Not Found')
        return redirect("/")
    for result in results:
        if town not in result:
            flash('Town Not Found')
            return redirect("/")
    # if the town is in the database, get the weather data
    site = results[0][1]  # get the site code
    pcode = results[0][2]  # get the pcode
    # create the url
    URL = f'https://dd.weather.gc.ca/citypage_weather/xml/{pcode}/{site}_e.xml'
    response = requests.get(URL)  # get the response
    # if the response is 404, redirect to the homepage with a flash message
    if response.status_code == 404:
        flash("No data available for the given location")
        return redirect("/")

    # if the response is 200, get the weather data
    weather = get_weather(response)
    hourly = get_hourly_forecast(response)
    almanac = get_almanac(response)
    sunstats = getSunRise(response)
    forecast_data = getForecast(response)
    city = getName(response)
    # render the weather.html template and pass the weather
    return render_template("weather.html", weather=weather, almanac=almanac, hourly=hourly, townresults=townresults, sunstats=sunstats, forecast_data=forecast_data, city=city)

# function to get the list of towns from the database


def get_weather(response):

    # create an xml element tree
    root = ET.fromstring(response.content)
    # get the current conditions element
    current_conditions = root.find('currentConditions')

    # get all the data
    # if the data is not available, set it to "no data"
    temperature = current_conditions.find('temperature')
    if temperature is not None:
        temperature = temperature.text
    else:
        temperature = "no data"
    # get the station name
    station = current_conditions.find('station')
    if station is not None:
        station = station.text
    else:
        station = "no data"
    # get wind speed
    wind_speed = current_conditions.find('wind/speed')
    if wind_speed is not None:
        wind_speed = wind_speed.text
    else:
        wind_speed = "no data"
    # get wind direction
    wind_direction = current_conditions.find('wind/direction')
    if wind_direction is not None:
        wind_direction = wind_direction.text
    else:
        wind_direction = "no data"
    # get wind bearing
    wind_bearing = current_conditions.find('wind/bearing')
    if wind_bearing is not None:
        wind_bearing = wind_bearing.text
    else:
        wind_bearing = "no data"
    # get condition
    condition = current_conditions.find('condition')
    if condition is not None:
        condition = condition.text
    else:
        condition = "no data"
    # get icon code
    iconcode = current_conditions.find('iconCode')
    if iconcode is not None:
        iconcode = iconcode.text
    else:
        iconcode = "no data"
    # get date and time
    textsummary = current_conditions.find('dateTime/timeStamp')
    if textsummary is not None:
        textsummary = textsummary.text
        date_string = textsummary
        date_time_obj = datetime.strptime(date_string, '%Y%m%d%H%M%S')
        date_time_12hr = date_time_obj.strftime('%Y %m %d %H %M %S')
        textsummary = date_time_12hr
    else:
        textsummary = "no data"
    # get dewpoint
    dewpoint = current_conditions.find('dewpoint')
    if dewpoint is not None:
        dewpoint = dewpoint.text
    else:
        dewpoint = "no data"
    # get humidity
    pressure = current_conditions.find('pressure')
    if pressure is not None:
        pressure = pressure.text
    else:
        pressure = "no data"
    # get visibility
    visibility = current_conditions.find('visibility')
    if visibility is not None:
        visibility = visibility.text
    else:
        visibility = "no data"
    # get relative humidity
    relative_humidity = current_conditions.find('relativeHumidity')
    if relative_humidity is not None:
        relative_humidity = relative_humidity.text
    else:
        relative_humidity = "no data"

    # return the data as a dict
    return {'temperature': temperature, 'wind_speed': wind_speed, 'wind_direction': wind_direction, 'wind_bearing': wind_bearing, 'condition': condition, 'iconcode': iconcode, 'textsummary': textsummary, 'station': station, 'dewpoint': dewpoint, 'pressure': pressure, 'visibility': visibility, 'relative_humidity': relative_humidity}


# function to get the hourly forecast
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

        # convert dateTimeUTC to format
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

# function to get the almanac data


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

# function to get the sun rise and set


def getSunRise(response):
    # create an xml element tree
    root = ET.fromstring(response.content)

    # Find the riseSet element
    rise_set = root.find("riseSet")

    # Initialize variables with "no info"
    sunrise_year = "no info"
    sunrise_month = "no info"
    sunrise_day = "no info"
    sunrise_hour = "no info"
    sunrise_minute = "no info"
    sunset_year = "no info"
    sunset_month = "no info"
    sunset_day = "no info"
    sunset_hour = "no info"
    sunset_minute = "no info"

    # If the riseSet element exists, extract the data
    if rise_set is not None:
        # Find the sunrise and sunset elements
        sunrise_element = rise_set.find("dateTime[@name='sunrise']")
        sunset_element = rise_set.find("dateTime[@name='sunset']")

        # Extract the year, month, day, hour, and minute elements from the sunrise and sunset elements
        sunrise_year = sunrise_element.find("year").text
        sunrise_month = sunrise_element.find("month").text
        sunrise_day = sunrise_element.find("day").text
        sunrise_hour = sunrise_element.find("hour").text
        sunrise_minute = sunrise_element.find("minute").text

        sunset_year = sunset_element.find("year").text
        sunset_month = sunset_element.find("month").text
        sunset_day = sunset_element.find("day").text
        sunset_hour = sunset_element.find("hour").text
        sunset_minute = sunset_element.find("minute").text

    # Create datetime objects for sunrise and sunset
    sunrise = datetime(int(sunrise_year), int(sunrise_month), int(
        sunrise_day), int(sunrise_hour), int(sunrise_minute))
    sunset = datetime(int(sunset_year), int(sunset_month), int(
        sunset_day), int(sunset_hour), int(sunset_minute))
    # Format the datetime objects
    sunrise = sunrise.strftime("%A %B %d, %Y at %I:%M %p")
    sunset = sunset.strftime("%A %B %d, %Y at %I:%M %p")
    sunstats = {
        'Sunrise': sunrise,
        'Sunset': sunset
    }
    return sunstats

# Get list of sites to return to web page


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

# get XML data from Environment Canada for the Forecast


def getForecast(response):
    root = ET.fromstring(response.content)
    forecast_data = []
    for forecast in root.findall('./forecastGroup/forecast'):
        forecast_dict = {}
        period = forecast.find('period')
        if period is not None:
            forecast_dict['period'] = period.text
        text_summary = forecast.find('textSummary')
        if text_summary is not None:
            forecast_dict['text_summary'] = text_summary.text
        cloud_precip = forecast.find('cloudPrecip/textSummary')
        if cloud_precip is not None:
            forecast_dict['cloud_precip'] = cloud_precip.text
        abbreviated_forecast = forecast.find('abbreviatedForecast/iconCode')
        if abbreviated_forecast is not None:
            forecast_dict['abbreviated_forecast'] = abbreviated_forecast.text
        temperatures = forecast.find('temperatures')
        if temperatures is not None:
            text_summary = temperatures.find('textSummary').text
            if text_summary is not None:
                forecast_dict['Temperature Summary'] = text_summary
            temperature = temperatures.find('temperature').text
            if temperature is not None:
                forecast_dict['Temperature'] = temperature
        winds = forecast.find('winds')
        if winds is not None:
            text_summary = winds.find('textSummary')
            if text_summary is not None:
                forecast_dict['Wind Summary'] = text_summary.text

            # Create an empty list to store the wind data
            wind_data = []

            # Iterate over the wind elements
            for wind in winds.findall('wind'):
                # Extract the speed, gust, direction, and bearing elements
                speed = wind.find('speed').text
                if speed is None:
                    speed = "no info"
                gust = wind.find('gust').text
                if gust is None:
                    gust = "no info"
                direction = wind.find('direction').text
                if direction is None:
                    direction = "no info"
                bearing = wind.find('bearing').text
                if bearing is None:
                    bearing = "no info"
                # Store the extracted data in a dictionary
                data = {
                    "Speed": speed + "km/h " + direction,
                    "Gusting": gust + "km/h" + direction,
                    "Bearing": bearing
                }

                # Add the dictionary to the wind_data list
                wind_data.append(data)

            # Add the wind_data list to the forecast_dict dictionary
            forecast_dict['Wind Data'] = wind_data

        relative_humidity = forecast.find('relativeHumidity')
        if relative_humidity is not None:
            forecast_dict['relative_humidity'] = relative_humidity.text
        wind_chill = forecast.find('windChill/textSummary')
        if wind_chill is not None:
            forecast_dict['wind_chill'] = wind_chill.text
        forecast_data.append(forecast_dict)
    return forecast_data

# get the name and region to display on the web page


def getName(response):
    root = ET.fromstring(response.content)
    location = root.find("location")
    name = location.find("name").text
    region = location.find("region").text
    return name, region


if __name__ == '__main__':
    app.run(host='0.0.0.0')
