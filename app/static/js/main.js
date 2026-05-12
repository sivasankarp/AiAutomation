/**
 * main.js  —  ContactForm App
 * Handles: char counter, loading spinner, live validation hints
 */

(function () {
  "use strict";

  /* ── Character counter ──────────────────────────────────────────────── */
  const messageField = document.getElementById("message");
  const charCounter  = document.getElementById("charCounter");
  const MAX_CHARS    = 2000;
  const WARN_CHARS   = 1800;

  if (messageField && charCounter) {
    function updateCounter() {
      const len = messageField.value.length;
      charCounter.textContent = `${len} / ${MAX_CHARS}`;
      charCounter.classList.toggle("warn",  len >= WARN_CHARS && len < MAX_CHARS);
      charCounter.classList.toggle("limit", len >= MAX_CHARS);
    }
    messageField.addEventListener("input", updateCounter);
    updateCounter(); // initialise on page load (in case of browser autofill)
  }


  /* ── Loading spinner on submit ──────────────────────────────────────── */
  const form      = document.getElementById("contactForm");
  const submitBtn = document.getElementById("submitBtn");

  if (form && submitBtn) {
    const btnText    = submitBtn.querySelector(".btn-text");
    const btnSpinner = submitBtn.querySelector(".btn-spinner");

    form.addEventListener("submit", function () {
      // Only show spinner if the browser is going to submit
      // (i.e. HTML5 validation passes — we rely on server-side too)
      if (form.checkValidity() !== false) {
        submitBtn.disabled = true;
        btnText.classList.add("d-none");
        btnSpinner.classList.remove("d-none");
      }
    });
  }


  /* ── Auto-dismiss flash alerts after 6 s ────────────────────────────── */
  document.querySelectorAll(".alert").forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 6000);
  });

})();
