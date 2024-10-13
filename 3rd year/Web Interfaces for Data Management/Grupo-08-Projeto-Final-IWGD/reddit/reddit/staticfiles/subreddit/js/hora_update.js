function formatNumber(number) {
    return number < 10 ? '0' + number : number;
}


function updateCurrentTime() {
    var now = new Date();
    var hours = formatNumber(now.getHours());
    var minutes = formatNumber(now.getMinutes());
    var seconds = formatNumber(now.getSeconds());
    var currentTimeString = hours + ':' + minutes + ':' + seconds;
    document.getElementById('current-time').textContent = currentTimeString;
}

setInterval(updateCurrentTime, 1000);


updateCurrentTime();