//prevent button from being pressed if user inputs town not in townresults
document.querySelector('button').addEventListener('click', function (e) {
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