document.addEventListener("DOMContentLoaded", () => {

// 🔥 SLIDER
let index = 0;
const slides = document.querySelectorAll(".slide");

if (slides.length > 0) {
    setInterval(() => {
        slides[index].classList.remove("active");
        index = (index + 1) % slides.length;
        slides[index].classList.add("active");
    }, 3500);
}

// 🔥 SCROLL ANIMATION
const elements = document.querySelectorAll(".card, .hero-text");

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

elements.forEach(el => observer.observe(el));

// 🔥 PARALLAX EFFECT
window.addEventListener("scroll", () => {
    const scroll = window.scrollY;
    document.querySelector(".hero").style.transform = `translateY(${scroll * 0.2}px)`;



});


    // 🔥 IMAGE PREVIEW
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("preview");

    if (fileInput && preview) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];

            if (file) {
                preview.src = URL.createObjectURL(file);
                preview.style.display = "block";
            }
        });
    }

});

window.addEventListener("load", () => {
const loader = document.getElementById("loader");
loader.style.display = "none";
});
