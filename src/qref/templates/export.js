(function () {
  var button = document.getElementById("save-evidence");
  var raw = document.getElementById("evidence-raw");
  var status = document.getElementById("save-status");
  if (!button || !raw || !window.Blob || !window.URL) { return; }
  button.hidden = false;
  button.addEventListener("click", function () {
    var blob = new Blob([raw.textContent], { type: "application/json" });
    var link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "evidence.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
    status.textContent = "Saved from the copy embedded in this page.";
  });
})();
