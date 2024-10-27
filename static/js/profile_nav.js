document.addEventListener('DOMContentLoaded', function() {
    const activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        activeLink.style.pointerEvents = 'none';
        activeLink.style.cursor = 'default';
    }
});