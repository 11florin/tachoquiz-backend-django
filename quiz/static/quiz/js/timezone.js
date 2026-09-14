"use strict";

function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    const trimmedCookie = cookie.trim();

    if (trimmedCookie.startsWith(`${name}=`)) {
      return decodeURIComponent(
        trimmedCookie.substring(name.length + 1)
      );
    }
  }

  return null;
}

const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const csrfToken = getCookie("csrftoken");

if (timezone && csrfToken) {
  fetch("/set-timezone/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrfToken,
    },
    body: new URLSearchParams({
      timezone: timezone,
    }),
  });
}