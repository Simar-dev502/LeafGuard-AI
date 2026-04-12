document.addEventListener("DOMContentLoaded", () => {

    // 🔥 SLIDER
    let index = 0;
    const slides = document.querySelectorAll(".slide");

    if (slides.length > 0) {
        setInterval(() => {
            slides[index].classList.remove("active");

            index = (index + 1) % slides.length;

            slides[index].classList.add("active");
        }, 3000);
    }

    // 🔥 SCROLL FUNCTIONS
    window.scrollToUpload = function () {
        const section = document.getElementById("upload");
        if (section) {
            section.scrollIntoView({ behavior: "smooth" });
        }
    };

    window.scrollToContact = function () {
        const section = document.getElementById("contact");
        if (section) {
            section.scrollIntoView({ behavior: "smooth" });
        }
    };

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