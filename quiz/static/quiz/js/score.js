"use strict";

const scoreBar = document.getElementById("score-bar");

if (scoreBar) {
  const percentage = Number.parseInt(
    scoreBar.dataset.percentage,
    10
  );

  if (Number.isInteger(percentage)) {
    const safePercentage = Math.min(
      Math.max(percentage, 0),
      100
    );

    requestAnimationFrame(() => {
      setTimeout(() => {
        scoreBar.style.width = `${safePercentage}%`;
      }, 100);
    });
  }
}