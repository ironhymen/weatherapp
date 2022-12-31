// collapse button functionality for the forecast and hourly forecast
const collapseButton = document.getElementById('collapse-button');
const forecastCollapseButton = document.getElementById('forecast-collapse-button');
const hourlyContainer = document.getElementById('hourly-container');
const forecastContainer = document.getElementById('forecast-container');
const forecastDays = document.querySelectorAll('.forecast-day');
const forecastDivs = document.querySelectorAll('.forecast');

// Set the initial state of the collapse button
let forecastCollapsed = true;
let hourlyCollapsed = true;

// Set the initial state of the forecast
forecastDivs.forEach((forecast, index) => {
    // Hide all but the first three forecasts
    if (forecastCollapsed && index > 2) {
        forecast.style.display = 'none';
    } else {
        forecast.style.display = 'block';
    }
});
// Add event listener to the collapse button
forecastCollapseButton.addEventListener('click', function () {
    // Toggle the state of the collapse button
    forecastCollapsed = !forecastCollapsed;
    forecastDivs.forEach((forecast, index) => {
        // Hide all but the first three forecasts
        if (forecastCollapsed && index > 2) {
            forecast.style.display = 'none';
        } else {
            forecast.style.display = 'block';
        }
    });
    // Update the text of the collapse button
    forecastCollapseButton.innerHTML = forecastCollapsed ? 'Expand' : 'Collapse';
});

// Set the initial state of the hourly forecast
forecastDays.forEach((forecast, index) => {
    if (hourlyCollapsed && index > 4) {
        // Hide all but the first five forecasts
        forecast.style.display = 'none';
    } else {
        forecast.style.display = 'block';
    }
});

//  Add event listener to the collapse button
collapseButton.addEventListener('click', function () {
    // Toggle the state of the collapse button
    hourlyCollapsed = !hourlyCollapsed;
    forecastDays.forEach((forecast, index) => {
        // Hide all but the first five forecasts
        if (hourlyCollapsed && index > 4) {
            forecast.style.display = 'none';
        } else {
            forecast.style.display = 'block';
        }
    });
    // Update the text of the collapse button
    collapseButton.innerHTML = hourlyCollapsed ? 'Expand' : 'Collapse';
});




// Draw the Compass and display on Screen
let bearing = document.getElementById('bearing').innerHTML;
let canvas = document.getElementById('compass');
let ctx = canvas.getContext('2d');

canvas.width = 250;
canvas.height = 250;
ctx.translate(125, 125); // move 0,0 to center
ctx.rotate(bearing * Math.PI / 180); // rotate according to bearing

// draw outer circle
ctx.fillStyle = '#000';
ctx.beginPath();
ctx.arc(0, 0, 122, 0, 2 * Math.PI);
ctx.strokeStyle = '#fff';
ctx.lineWidth = 0.05; // make the circle less thick
ctx.fill();

// draw inner circle
ctx.fillStyle = '#dfdfdf';
ctx.beginPath();
ctx.arc(0, 0, 118, 0, 2 * Math.PI);
ctx.fill();

// draw line
if (bearing !== "None") {
    ctx.strokeStyle = '#000';
    ctx.fillStyle = "#ff0000";
    ctx.beginPath();
    ctx.moveTo(0, -90);  // start at the TIP of the triangle
    ctx.lineTo(-10, 0);  // draw the left point of the triangle
    ctx.lineTo(10, 0);  // draw the right point of the triangle
    ctx.closePath();  // draw a line back to the start to complete the triangle
    ctx.fill();  // fill the triangle with the current fill style
    ctx.strokestyle = "#000";
    ctx.fillStyle = "#000";
    ctx.beginPath();
    ctx.moveTo(0, 90);
    ctx.lineTo(-10, 0);
    ctx.lineTo(10, 0);
    ctx.closePath();
    ctx.fill();
} else {
    // Set the fill color to black
    ctx.fillStyle = "#000";
    ctx.font = "bold 30px 'Helvetica Neue', sans-serif";
    ctx.fillText("None", -30, 10)
}

// save current transform
ctx.save();
ctx.setTransform(1, 0, 0, 1, 0, 0)
ctx.translate(125, 125)

// draw the N, S, E, W
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.fillStyle = "#ff0000";
ctx.font = "bold 45px 'Helvetica Neue', sans-serif";
ctx.fillText("N", 0, -95);
ctx.fillStyle = "#000";
ctx.fillText("S", 0, 95);
ctx.fillText("E", 95, 0);
ctx.fillText("W", -87, 0);

// restore transform to exclude the bearing rotation
ctx.restore();

// Draw the Compass and display on Screen inside each forecast
const forecastElements = document.querySelectorAll('.forecast');

forecastElements.forEach(forecastElement => {
    // Get the canvas elements and the bearing elements inside the forecast div
    const canvasElements = forecastElement.querySelectorAll('.forecast-compass');
    const bearingElements = forecastElement.querySelectorAll('.fbearing');

    // Iterate over the canvas elements and draw the compass for each one
    canvasElements.forEach((canvasElement, index) => {
        // Get the canvas context and the bearing value
        const ctx = canvasElement.getContext('2d');
        const bearing = bearingElements[index].innerHTML;

        // Set the canvas dimensions and rotate the context according to the bearing
        canvasElement.width = 250;
        canvasElement.height = 250;
        ctx.translate(125, 125);
        ctx.rotate(bearing * Math.PI / 180);

        // Draw the outer circle
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(0, 0, 122, 0, 2 * Math.PI);
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 0.05;
        ctx.fill();

        // Draw the inner circle
        ctx.fillStyle = '#dfdfdf';
        ctx.beginPath();
        ctx.arc(0, 0, 118, 0, 2 * Math.PI);
        ctx.fill();

        // Draw the line
        if (bearing !== "no data" && bearing !== "no info") {
            ctx.strokeStyle = '#000';
            ctx.fillStyle = "#ff0000";
            ctx.beginPath();
            ctx.moveTo(0, -90);
            ctx.lineTo(-10, 0);
            ctx.lineTo(10, 0);
            ctx.closePath();
            ctx.fill();
            ctx.strokestyle = "#000";
            ctx.fillStyle = "#000";
            ctx.beginPath();
            ctx.moveTo(0, 90);
            ctx.lineTo(-10, 0);
            ctx.lineTo(10, 0);
            ctx.closePath();
            ctx.fill();
        } else {
            // Set the fill color to yellow
            ctx.fillStyle = "#000";
            ctx.font = "bold 30px 'Helvetica Neue', sans-serif";
            ctx.fillText("None", -30, 10)
        }

        // Save the current transform
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.translate(125, 125);

        // Draw the N, S, E, W
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "#ff0000";
        ctx.font = "bold 45px 'Helvetica Neue', sans-serif";
        ctx.fillText("N", 0, -95);
        ctx.fillStyle = "#000";
        ctx.fillText("S", 0, 95);
        ctx.fillText("E", 95, 0);
        ctx.fillText("W", -87, 0);

        // Restore the transform to exclude the bearing rotation
        ctx.restore();
    });
});






// Convert temperatures on page to degrees Fahrenheit
function convertToFahrenheit() {
    // Get the elements with the class "celcius"
    var celciusElements = document.getElementsByClassName("celcius");

    // Iterate over the elements
    for (var i = 0; i < celciusElements.length; i++) {
        // Get the current element
        var element = celciusElements[i];

        // Check if the element has already been converted
        if (!element.classList.contains("converted")) {
            // Get the text content of the element
            var text = element.textContent;

            // Split the text into an array of substrings
            var substrings = text.split("°C");

            // Get the first substring (the temperature in degrees Celsius)
            var celsius = substrings[0];

            // Convert the temperature to degrees Fahrenheit
            var fahrenheit = celsius * 9 / 5 + 32;

            // Round the temperature to two decimal places
            var roundedFahrenheit = Math.round(fahrenheit * 100) / 100;

            // Update the element's text content with the temperature in degrees Fahrenheit
            element.textContent = roundedFahrenheit + "°F";

            // Add the "converted" class to the element
            element.classList.add("converted");
        }
    }
}


// Convert temperatures on page to degrees Celsius
function convertToCelcius() {
    // Get the elements with the class "celcius"
    var celciusElements = document.getElementsByClassName("celcius");

    // Iterate over the elements
    for (var i = 0; i < celciusElements.length; i++) {
        // Get the current element
        var element = celciusElements[i];

        // Check if the element has already been converted
        if (element.classList.contains("converted")) {
            // Get the text content of the element
            var text = element.textContent;

            // Split the text into an array of substrings
            var substrings = text.split("°F");

            // Get the first substring (the temperature in degrees Fahrenheit)
            var fahrenheit = substrings[0];

            // Convert the temperature to degrees Celsius
            var celsius = (fahrenheit - 32) * 5 / 9;

            // Round the temperature to two decimal places
            var roundedCelsius = Math.round(celsius * 100) / 100;

            // Update the element's text content with the temperature in degrees Celsius
            element.textContent = roundedCelsius + "°C";

            // Add the "converted" class to the element
            element.classList.remove("converted");
        }
    }
}




// Convert dates to local time zone

// Select all elements that contain dates
const dateElements = document.querySelectorAll('[data-date]');

// Convert the date in each element to the user's local time zone
dateElements.forEach(element => {
    // Get the date string from the element
    const dateString = element.dataset.date;
    const timePieces = dateString.split(" ");
    const year = timePieces[0];
    const month = (timePieces[1] - 1);
    const day = timePieces[2];
    const hours = timePieces[3];
    const minutes = timePieces[4];
    const seconds = timePieces[5];
    // Convert the date string to a date

    const date = new Date();
    date.setUTCFullYear(year);
    date.setUTCMonth(month);
    date.setUTCDate(day);
    date.setUTCHours(hours);
    date.setUTCMinutes(minutes);
    date.setUTCSeconds(seconds);

    // Format the date using the toLocaleString method
    const formattedDate = date.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    });

    // Replace the text content of the element with the formatted date
    element.textContent = formattedDate;
});

