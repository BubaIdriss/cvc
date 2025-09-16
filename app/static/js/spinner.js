// Reset the spinner when the page loads
window.onload = function () {
    document.getElementById('loading-spinner').style.display = 'none';
    document.getElementById('loading-overlay').style.display = 'none';
};

// JavaScript to handle the loading state
document.addEventListener('DOMContentLoaded', function () {
    // Select all buttons and links
    const buttonsAndLinks = document.querySelectorAll('button, a');

    buttonsAndLinks.forEach(element => {
        element.addEventListener('click', function (event) {
            // Prevent default action if needed
            // event.preventDefault();

            // Show the loading spinner and overlay
            document.getElementById('loading-spinner').style.display = 'block';
            document.getElementById('loading-overlay').style.display = 'block';

            // Hide the spinner after 40 seconds or 1 minute
            setTimeout(function () {
                document.getElementById('loading-spinner').style.display = 'none';
                document.getElementById('loading-overlay').style.display = 'none';
            }, 3000); // 40 seconds (change to 60000 for 1 minute)
        });
    });
});