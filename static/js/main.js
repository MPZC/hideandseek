// static/js/main.js
// Zachowanie: przy zmianie przełącznika wykonujemy GET /?mode=encode lub /?mode=decode
// Dzięki temu backend wykona reset_state() podczas GET i strona załaduje się "czysta".

document.addEventListener("DOMContentLoaded", function () {
  const switchEl = document.getElementById("modeSwitch");
  if (!switchEl) return;

  // Gdy użytkownik zmienia tryb — przekieruj na GET z parametrem mode
  switchEl.addEventListener("change", function (e) {
    const mode = switchEl.checked ? "decode" : "encode";
    // Jeśli już jesteśmy na tym trybie — nic nie rób
    const currentSearch = new URLSearchParams(window.location.search);
    if (currentSearch.get("mode") === mode) {
      // ale i tak wymuśmy reload, by pozbyć się ewentualnego stanu w JS
      window.location.href = `${window.location.pathname}?mode=${mode}`;
      return;
    }
    // przekierowanie GET -> backend zresetuje stan i wyrenderuje czyste panele
    window.location.href = `${window.location.pathname}?mode=${mode}`;
  });

  // (opcjonalne) kliknięcie etykiety też powinno zmieniać checkbox — pozostawiamy domyślne zachowanie
});
