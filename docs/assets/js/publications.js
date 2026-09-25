// "Copy citation" buttons on the publications list. The buttons ship hidden
// and are only shown when the browser can write to the clipboard.
(function () {
  if (!navigator.clipboard || !window.isSecureContext) return;

  document.querySelectorAll(".pub-cite").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(btn.dataset.citation).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy citation"; }, 1800);
      });
    });
  });
})();
