/**
 * XMacro Node.js Sidecar + AI Guardian runtime
 * Port: 17841 — affiche les logs dans le terminal PyCharm
 */

const http = require("http");
const { analyze } = require("./analyzer");

const PORT = 17841;
const MAX_EVENTS = 500;
const events = [];

function ts() {
  return new Date().toISOString().slice(11, 23);
}

function colorForTag(tag) {
  const colors = {
    AI: "\x1b[95m",
    ENGINE: "\x1b[36m",
    MOUSE: "\x1b[33m",
    KEYBOARD: "\x1b[35m",
    TOGGLE: "\x1b[93m",
    NODE: "\x1b[92m",
    FATAL: "\x1b[91m",
    PROXY: "\x1b[92m",
    DEBUG: "\x1b[90m",
  };
  return colors[tag] || "\x1b[37m";
}

function logEvent(tag, msg, extra = {}) {
  const color = colorForTag(tag);
  const reset = "\x1b[0m";
  const extraStr = Object.keys(extra).length
    ? " | " + Object.entries(extra).map(([k, v]) => `${k}=${v}`).join(" ")
    : "";
  const line = `[${ts()}] [${tag}] ${msg}${extraStr}`;
  console.log(`${color}${line}${reset}`);
  events.push({ ts: Date.now(), tag, msg, extra });
  if (events.length > MAX_EVENTS) events.shift();
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

function json(res, code, data) {
  res.writeHead(code, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  });
  res.end(JSON.stringify(data));
}

const server = http.createServer(async (req, res) => {
  const path = req.url.split("?")[0];

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    });
    res.end();
    return;
  }

  if (path === "/health" && req.method === "GET") {
    json(res, 200, { status: "ok", events: events.length, port: PORT });
    return;
  }

  if (path === "/api/events" && req.method === "GET") {
    json(res, 200, { events: events.slice(-100) });
    return;
  }

  if (path === "/api/analyze" && req.method === "POST") {
    try {
      const raw = await readBody(req);
      const { project, fix } = JSON.parse(raw);
      logEvent("AI", `Analyse demandée: ${project}`);
      const result = analyze(project, !!fix);
      json(res, 200, result);
    } catch (err) {
      json(res, 400, { error: err.message });
    }
    return;
  }

  if (path === "/api/log" && req.method === "POST") {
    try {
      const raw = await readBody(req);
      const payload = JSON.parse(raw);
      logEvent(payload.tag || "LOG", payload.msg || "", payload.extra || {});
      json(res, 200, { ok: true });
    } catch (err) {
      json(res, 400, { error: err.message });
    }
    return;
  }

  json(res, 404, { error: "not found" });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`\x1b[92m[NODE] AI Guardian sidecar → http://127.0.0.1:${PORT}\x1b[0m`);
  logEvent("NODE", "Prêt — en attente des logs Python");
});

process.on("SIGTERM", () => {
  logEvent("NODE", "Arrêt");
  server.close();
  process.exit(0);
});
