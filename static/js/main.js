document.addEventListener("DOMContentLoaded", function () {
  const switchEl = document.getElementById("modeSwitch");
  if (!switchEl) return;

  switchEl.addEventListener("change", function (e) {
    const mode = switchEl.checked ? "decode" : "encode";
    const currentSearch = new URLSearchParams(window.location.search);
    if (currentSearch.get("mode") === mode) {
      window.location.href = `${window.location.pathname}?mode=${mode}`;
      return;
    }
    window.location.href = `${window.location.pathname}?mode=${mode}`;
  });
});
