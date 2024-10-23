window.addEventListener('load', function () {
    var spinner = document.getElementById('spinner');

    var delay = 1500;

    setTimeout(function () {
        spinner.classList.add('hidden');
    }, delay);
});