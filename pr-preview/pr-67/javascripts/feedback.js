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
      var body = JSON.stringify({ path: path, release: releaseFromPath(), vote: vote });
      root.classList.add("is-busy");
      // CloudFront OAC requires this header on the POST. Hash the exact
      // string that is sent as the body. Without subtle, do not send.
      var hashing = null;
      try {
        if (typeof crypto !== "undefined" && crypto.subtle && typeof crypto.subtle.digest === "function") {
          hashing = crypto.subtle.digest("SHA-256", new TextEncoder().encode(body)).then(function (digest) {
            var bytes = new Uint8Array(digest);
            var hex = "";
            for (var i = 0; i < bytes.length; i++) {
              hex += ("0" + bytes[i].toString(16)).slice(-2);
            }
            return hex;
          });
        }
      } catch (error) {
        hashing = null;
      }
      if (!hashing) {
        root.classList.remove("is-busy");
        return;
      }
      hashing.then(function (hex) {
        return fetch(endpoint, {
          method: "POST",
          redirect: "manual",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "x-amz-content-sha256": hex
          },
          body: body
        });
      }).then(function (response) {
        // 204 is the only stored vote. A missing cookie is HTTP 200 (the
        // sign-in page); 400 and 405 are errors. redirect:manual keeps a
        // redirect from turning into that 200.
        if (!response || response.status !== 204) {
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
