"use strict"

const answerInputs = document.querySelectorAll(
  'input[name="answer"]'
);

const checkAnswerBtn = document.getElementById(
  "check-answer-btn"
);

if (checkAnswerBtn) {
  answerInputs.forEach((input) => {
    input.addEventListener("change", () => {
      checkAnswerBtn.disabled = false;
    });
  });
}