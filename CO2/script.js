// Add your JavaScript code for handling the modal here
function openSignUpModal() {
    document.getElementById("SignUpModal").style.display = "block";
}

function closeSignUpModal() {
    document.getElementById("SignUpModal").style.display = "none";
}

function openLoginModal() {
    document.getElementById("loginModal").style.display = "block";
}

function closeLoginModal() {
    document.getElementById("loginModal").style.display = "none";
}

window.onscroll = function () {
    stickNavbar();
};

var navbar = document.querySelector('.navbar');
var sticky = navbar.offsetTop;

function stickNavbar() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add('sticky');
    } else {
        navbar.classList.remove('sticky');
    }
}

function openBotPage() {
    // Change "nextPage.html" to the filename of your next HTML file
    window.location.href = 'index2.html';
}

function openHealthPage() {
    window.location.href = 'index3.html';
}