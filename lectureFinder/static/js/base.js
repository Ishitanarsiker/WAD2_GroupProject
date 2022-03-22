// Log-in pop-up

let modal1 = document.getElementById('id01');
let modal2 = document.getElementById('id02');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target === modal1) {
        modal1.style.display = "none";
    }
    if (event.target === modal2) {
        modal2.style.display = "none";
    }
}

var theme = document.querySelector("#theme-link");
var currentTheme = localStorage.getItem("currentTheme");


loadTheme();

function loadTheme() {
    if (currentTheme == "dark") {
        theme.setAttribute('href', "/static/css/dark.css");
        console.log("Current Theme : Dark");
        logo.src = "/static/images/logo-white.png";
    } else {
        theme.setAttribute('href', "/static/css/light.css");
        console.log("Current Theme : Light");
        logo.src = "/static/images/logo-black.png";
    }
}

function ToggleTheme() {
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

    if (prefersDarkScheme.matches) {
        window.matchMedia("(prefers-color-scheme: light)").matches ? 'light' : 'dark';
    } else {
        window.matchMedia("(prefers-color-scheme: dark)").matches ? 'dark' : 'light';
    }
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('currentTheme', newTheme);
    location.reload();
}