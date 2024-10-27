document.addEventListener('DOMContentLoaded', function() {
    const activeNavLink = document.querySelector('#navbarNav .nav-link.active');
    if (activeNavLink) {
        activeNavLink.style.pointerEvents = 'none';
        activeNavLink.style.cursor = 'default';
    }
});