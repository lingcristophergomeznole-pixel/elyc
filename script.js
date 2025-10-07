let currentIndex = 0;
const slides = document.getElementById("slides");
const images = slides.getElementsByTagName("img");

function showSlide(index) {
  if (index >= images.length) currentIndex = 0;
  else if (index < 0) currentIndex = images.length - 1;
  else currentIndex = index;
  slides.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function moveSlide(step) {
  showSlide(currentIndex + step);
}

setInterval(() => moveSlide(1), 4000);
