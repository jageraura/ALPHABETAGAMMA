const carousel = document.querySelector('.carousel');
let index = 0;

function slideImages() {
    index++;
    if (index > carousel.children.length - 1) {
        index = 0;
    }
    carousel.style.transform = `translateX(-${index * 100}%)`;
}

setInterval(slideImages, 3000);

document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".hamburger-menu");
    const mobileMenu = document.getElementById("mobile-menu");

    // Toggle the menu visibility when clicking the hamburger button
    menuButton.addEventListener("click", function () {
        mobileMenu.classList.toggle("active");
    });
});
