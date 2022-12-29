//prevent button from being pressed if user inputs town not in townresults
document.querySelector('townselect').addEventListener('click', function (e) {
    var townsearch = document.querySelector('#townsearch-input').value;
    var townresults = document.querySelector('#sitelist').options;
    var townresultsArray = [];
    for (var i = 0; i < townresults.length; i++) {
        townresultsArray.push(townresults[i].value);
    }
    if (townresultsArray.indexOf(townsearch) === -1) {
        e.preventDefault();
        // insert error message above search-site div
        var errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.innerHTML = 'Please select a town from the list';
        var searchSiteDiv = document.querySelector('.search-site');
        searchSiteDiv.parentNode.insertBefore(errorDiv, searchSiteDiv);
        // remove error message after 3 seconds
        setTimeout(function () {
            errorDiv.parentNode.removeChild(errorDiv);
        }, 3000);
    }
});


// Select the input element with the ID "custom-dropdown"
const input = document.querySelector('#custom-dropdown');

// Listen for changes to the input element
input.addEventListener('input', (event) => {
    // Get the list of options from the "data-list" attribute
    const options = event.target.getAttribute('data-list').split(',');

    // Iterate through the options
    options.forEach((option) => {
        // If the option does not match the current value of the input element,
        // filter it out of the list of options
        if (option !== event.target.value) {
            event.target.setAttribute('data-list', options.filter((o) => o !== option).join(','));
        }
    });
});