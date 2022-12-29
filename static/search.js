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