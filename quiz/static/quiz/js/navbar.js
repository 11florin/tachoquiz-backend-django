'use strict';

// Navbar Hamburger

const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const navList = document.querySelector('#nav-menu ul');

hamburger.addEventListener('click', function() {
    const isOpen = navMenu.classList.toggle('open');

    hamburger.setAttribute('aria-expanded', isOpen);
    hamburger.setAttribute(
        'aria-label',
        isOpen ? 'Close menu' : 'Open menu'
    );
});

navList.addEventListener('click', function(e) {
    if (e.target.tagName === 'A') {
        navMenu.classList.remove('open');

        hamburger.setAttribute('aria-expanded', false);
        hamburger.setAttribute('aria-label', 'Open menu');
    }
});