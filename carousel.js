let index = 0;
const images = document.querySelectorAll('.carousel-images img');
const totalImages = images.length;

function showNextImage() {
    images[index].classList.remove('active');
    index = (index + 1) % totalImages;
    images[index].classList.add('active');
}

setInterval(showNextImage, 1500);
