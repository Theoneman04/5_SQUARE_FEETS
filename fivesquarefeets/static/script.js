let slideIndex = 0;
let slides = document.getElementsByClassName("slide-new");
showSlides();

function showSlides() {
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1; }
    slides[slideIndex - 1].style.display = "block";

    // Change the time interval to 7 seconds (7000 milliseconds)
    setTimeout(showSlides, 7000);
}

// For previous/next controls
function plusSlides(n) {
    slideIndex += n - 1; // Adjust for 0-based index
    if (slideIndex >= slides.length) { slideIndex = 0; }
    if (slideIndex < 0) { slideIndex = slides.length - 1; }
    showSlides();
}




