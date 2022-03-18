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

// members page menu

function swapToS() {
    document.getElementById("m").style.display = "none";
    document.getElementById("s").style.display = "block";
}

function swapToM() {
    document.getElementById("m").style.display = "block";
    document.getElementById("s").style.display = "none";
}

