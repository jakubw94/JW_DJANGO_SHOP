document.addEventListener('DOMContentLoaded', function () {
    var videoModal = document.getElementById('videoModal');
    var videoIframe = document.getElementById('productVideo');
    var videoSrc = videoIframe.src;

    videoModal.addEventListener('hidden.bs.modal', function () {
        videoIframe.src = '';
    });

    videoModal.addEventListener('shown.bs.modal', function () {
        videoIframe.src = videoSrc;
    });
});

// Funkcja do obsługi błędu ładowania wideo
function handleVideoError(youtubeUrl) {
    // Zamknij modal
    var videoModal = document.getElementById('videoModal');
    var modal = bootstrap.Modal.getInstance(videoModal);
    if (modal) {
        modal.hide();
    }

    // Otwórz YouTube w nowej karcie
    window.open(youtubeUrl, '_blank');
}

document.addEventListener('DOMContentLoaded', () => {
  // Usuń wszystkie klucze sessionStorage zaczynające się od "bs.carousel"
  for (let key in sessionStorage) {
    if (key.startsWith('bs.carousel')) {
      sessionStorage.removeItem(key);
    }
  }
});

window.addEventListener('load', () => {
  const activeSlide = document.querySelector('#carouselExampleIndicators .carousel-item.active');
  if (activeSlide && activeSlide.offsetLeft !== 0) {
    // Widać, że slider jest przesunięty – wymuś twarde odświeżenie
    window.location.reload(true);
  }
});