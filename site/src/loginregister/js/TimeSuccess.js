// Function to make "Time Success" Alert to disappear after 5 seconds.

window.onload = function()
{
    timedHide(document.getElementById('changeSuccess'), 5);

}

function timedHide(element, seconds)
{
    if (element) {
        setTimeout(function() {
        element.style.display = 'none';
        }, seconds*1000);
    }
}