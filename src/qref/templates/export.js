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

(function () {
  // Links from findings point into collapsed <details>; open the enclosing sections so the target is visible.
  function reveal() {
    var id = decodeURIComponent(location.hash.slice(1));
    var target = id && document.getElementById(id);
    if (!target) { return; }
    for (var node = target.parentElement; node; node = node.parentElement) {
      if (node.tagName === "DETAILS") { node.open = true; }
    }
    target.scrollIntoView();
  }
  window.addEventListener("hashchange", reveal);
  reveal();
})();
