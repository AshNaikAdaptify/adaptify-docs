const assert = require("assert");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const test = require("node:test");
const vm = require("vm");

const scriptPath = path.join(__dirname, "..", "docs", "javascripts", "feedback.js");
const source = fs.readFileSync(scriptPath, "utf8");

function expectedHex(body) {
  return crypto.createHash("sha256").update(body, "utf8").digest("hex");
}

function load(options) {
  const calls = [];
  const classes = new Set(["adaptify-vote"]);
  const root = {
    getAttribute(name) {
      if (name === "data-endpoint") return "/_feedback";
      if (name === "data-path") return options.pagePath || "/get-started/";
      return null;
    },
    classList: {
      contains(name) { return classes.has(name); },
      add(name) { classes.add(name); },
      remove(name) { classes.delete(name); },
    },
    addEventListener(type, fn) {
      if (type === "click") root.click = fn;
    },
  };
  const button = {
    getAttribute(name) { return name === "data-vote" ? "up" : null; },
    closest(selector) { return selector === "button[data-vote]" ? button : null; },
  };
  const context = {
    document: {
      querySelectorAll() { return [root]; },
    },
    window: { location: { pathname: options.pathname || "/get-started/" } },
    crypto: options.crypto === undefined ? globalThis.crypto : options.crypto,
    TextEncoder,
    Uint8Array,
    JSON,
    Promise,
    fetch(url, init) {
      calls.push({ url, init });
      return Promise.resolve({ status: options.status === undefined ? 204 : options.status });
    },
  };
  vm.createContext(context);
  vm.runInContext(source, context);
  return {
    calls,
    classes,
    click() { root.click({ target: button }); },
  };
}

function settle() {
  return new Promise((resolve) => setTimeout(resolve, 30));
}

test("POST body is hashed into x-amz-content-sha256 and sent unchanged", async () => {
  const page = load({ pathname: "/get-started/", status: 204 });
  page.click();
  await settle();
  assert.strictEqual(page.calls.length, 1);
  const init = page.calls[0].init;
  const body = '{"path":"/get-started/","release":"","vote":"up"}';
  assert.strictEqual(init.body, body);
  assert.strictEqual(init.method, "POST");
  assert.strictEqual(init.redirect, "manual");
  assert.strictEqual(init.credentials, "same-origin");
  assert.strictEqual(init.headers["Content-Type"], "application/json");
  assert.strictEqual(init.headers["x-amz-content-sha256"], expectedHex(body));
  assert.ok(page.classes.has("is-sent"));
  assert.ok(!page.classes.has("is-busy"));
});

test("a live path with no release prefix sends an empty release", async () => {
  const page = load({ pathname: "/", pagePath: "/", status: 204 });
  page.click();
  await settle();
  const body = '{"path":"/","release":"","vote":"up"}';
  assert.strictEqual(page.calls[0].init.body, body);
  assert.strictEqual(page.calls[0].init.headers["x-amz-content-sha256"], expectedHex(body));
});

test("an RC path still sends that release number", async () => {
  const page = load({ pathname: "/_rc/7/get-started/", status: 204 });
  page.click();
  await settle();
  const body = '{"path":"/get-started/","release":"7","vote":"up"}';
  assert.strictEqual(page.calls[0].init.body, body);
  assert.strictEqual(page.calls[0].init.headers["x-amz-content-sha256"], expectedHex(body));
});

test("HTTP 200, 400, and 405 do not show the thank-you state", async () => {
  for (const status of [200, 400, 405]) {
    const page = load({ status });
    page.click();
    await settle();
    assert.strictEqual(page.calls.length, 1, String(status));
    assert.ok(!page.classes.has("is-sent"), String(status));
    assert.ok(!page.classes.has("is-busy"), String(status));
  }
});

test("missing crypto.subtle does not send the vote", async () => {
  const page = load({ crypto: {} });
  page.click();
  await settle();
  assert.strictEqual(page.calls.length, 0);
  assert.ok(!page.classes.has("is-sent"));
  assert.ok(!page.classes.has("is-busy"));
});
