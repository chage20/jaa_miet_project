document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('carouselTrack');
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');

    if (!track || !prevBtn || !nextBtn) return;

    const cards = Array.from(track.children);
    const cardWidth = cards[0].offsetWidth + 30;
    let currentIndex = 0;
    const visibleCards = 3;

    function scrollNext() {
        currentIndex++;

        if (currentIndex > cards.length - visibleCards) {
            currentIndex = 0;
        }

        track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
    }

    function scrollPrev() {
        currentIndex--;

        if (currentIndex < 0) {
            currentIndex = cards.length - visibleCards;
        }

        track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
    }

    prevBtn.addEventListener('click', scrollPrev);
    nextBtn.addEventListener('click', scrollNext);
});