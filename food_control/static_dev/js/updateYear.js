document.addEventListener("DOMContentLoaded", function () {
    const elem = document.getElementById("year");
    const server_time = new Date(elem.dataset.time);
    const js_time = new Date();
    const time_delta = Math.abs(js_time - server_time);
    const hours_10 = 10 * 60 * 60 * 1000
    if (time_delta <= hours_10) {
        elem.textContent = js_time.getFullYear();
    }
});