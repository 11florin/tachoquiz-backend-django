'use strict';

// Navbar Hamburger

const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const navList = document.querySelector('#nav-menu ul');

function setMenuState(isOpen) {
    navMenu.classList.toggle('open', isOpen);
    navMenu.setAttribute('aria-hidden', String(!isOpen));
    navMenu.inert = !isOpen;
    hamburger.setAttribute('aria-expanded', String(isOpen));
    hamburger.setAttribute(
        'aria-label',
        isOpen ? 'Close menu' : 'Open menu'
    );
}

setMenuState(window.innerWidth >= 768);

hamburger.addEventListener('click', function() {
    setMenuState(!navMenu.classList.contains('open'));
});

navList.addEventListener('click', function(e) {
    if (e.target.tagName === 'A') {
        setMenuState(false);
    }
});

window.addEventListener('resize', function() {
    if (window.innerWidth >= 768) {
        navMenu.inert = false;
        navMenu.setAttribute('aria-hidden', 'false');
    } else if (!navMenu.classList.contains('open')) {
        navMenu.inert = true;
        navMenu.setAttribute('aria-hidden', 'true');
    }
});