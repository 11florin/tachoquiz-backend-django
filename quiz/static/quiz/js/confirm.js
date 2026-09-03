"use strict";

// Read username saved during login
const user = localStorage.getItem("tq_user");

// Defensive design: if no username, redirect to login
if (!user) {
  alert("No login session found. Please log in first.");
  // location.replace("login.html");
  // return;
  window.location.href = "login.html";
  throw new Error("No username found");
}
// Personalize welcome message
const title = document.getElementById("welcome-title");
title.textContent = `Welcome ${user}`;

const text = document.getElementById("confirm-text");
text.textContent = `${user}, your login was successful.`;
