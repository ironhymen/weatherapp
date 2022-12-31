# Boreas Weather App

Welcome to Boreas Weather, an app created as a final project for the CS50 course. It is designed to help you stay informed about the weather at your cabin destination in Canada. All of the weather information displayed on the app is sourced from Environment Canada. Please note that only Canadian weather stations are included in the app.

[Video Demo:](https://www.youtube.com/watch?v=zyHU9IxZp_Q)

Video Demo: https://www.youtube.com/watch?v=zyHU9IxZp_Q

## Why "Boreas"?

The name "Boreas" was chosen for this app because it is the Greek god of the north wind and bringer of cold winter air. As this app is designed to help cabin goers stay informed about the weather, particularly in colder climates, the name "Boreas" seemed like a fitting choice.

## Getting Started

To use the app, simply visit [http://weather.sagresnaw.art/](http://weather.sagresnaw.art/) and follow the prompts. You can enter the name of the town or select from our list of available towns in the database to view the current weather conditions.

## Configuration

No configuration is needed to use this app when accessing it through the web. However, if you want to run the app locally on your own computer, you will need to set up a local development environment and configure the app accordingly. 

To set up the local development environment, you will need to install Python 3, Flask, and all required dependencies. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
Once all dependencies are installed, you can start the local server by running the following command in the root directory of the app:

```bash
export FLASK_APP=app
flask run
```
The app should now be running on your local server at http://localhost:5000.

## Compilation

This app does not need to be compiled, as it is a web-based application that can be accessed through a web browser. When running the app locally, the Python code is interpreted by the local development server.

## Usage

To use the app, follow these steps:

1. Visit [http://localhost:5000](http://localhost:5000) in your web browser (if running the app locally) or [http://weather.sagresnaw.art/](http://weather.sagresnaw.art/) (if accessing the app through the web).
2. Enter the name of the town or select from the list of available towns in the database.
3. View the current weather conditions for the selected town.

## Support

If you have any questions or encounter any issues while using the app, please don't hesitate to contact me.