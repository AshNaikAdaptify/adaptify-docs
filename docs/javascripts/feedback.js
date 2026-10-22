/* Customer page votes. Posts {path, release, vote} and toggles classes only. */
(function () {
  var widgets = document.querySelectorAll("[data-adaptify-vote]");

  function releaseFromPath() {
    var match = window.location.pathname.match(/\/_rc\/(\d+)(?:\/|$)/);
    return match ? match[1] : "";
  }

  widgets.forEach(function (root) {
    root.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-vote]");
      if (!button || root.classList.contains("is-sent") || root.classList.contains("is-busy")) {
        return;
      }
      var vote = button.getAttribute("data-vote");
      if (vote !== "up" && vote !== "down") {
        return;
      }
      var endpoint = root.getAttribute("data-endpoint") || "/_feedback";
      var path = root.getAttribute("data-path") || "/";
      root.classList.add("is-busy");
      fetch(endpoint, {
        method: "POST",
        redirect: "manual",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: path, release: releaseFromPath(), vote: vote })
      }).then(function (response) {
        // 204 is the only stored vote. A missing cookie is HTTP 200 (the
        // sign-in page); 400 and 405 are errors. redirect:manual keeps a
        // redirect from turning into that 200.
        if (response.status !== 204) {
          throw new Error("feedback not stored");
        }
        root.classList.add("is-sent");
      }).catch(function () {
        /* Leave the buttons in place. No error is shown. */
      }).then(function () {
        root.classList.remove("is-busy");
      });
    });
  });
})();
