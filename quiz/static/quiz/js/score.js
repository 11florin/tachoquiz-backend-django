"use strict";

const scoreBar = document.getElementById("score-bar");

if (scoreBar) {
    const percentage = scoreBar.dataset.percentage;
    scoreBar.style.width = `${percentage}%`;
}