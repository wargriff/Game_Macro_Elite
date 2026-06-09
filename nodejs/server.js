/**
 * Node.js bridge — port 5173
 * Sert Mission Control + proxy vers API Python (17840)
 */
const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const path = require("path");

const PORT = process.env.XCLICKER_NODE_PORT || 5173;
const PYTHON_API = process.env.XCLICKER_API_URL || "http://127.0.0.1:17840";

const app = express();
app.use(express.json());

// Proxy API Python
app.use(
  "/api",
  createProxyMiddleware({
    target: PYTHON_API,
    changeOrigin: true,
    pathRewrite: (p) => p.replace(/^\/api/, "/api"),
    onError(err, _req, res) {
      console.error("[NODE] proxy error:", err.message);
      res.status(502).json({ status: "offline", error: err.message });
    },
  })
);

app.use(
  "/api/v1",
  createProxyMiddleware({
    target: PYTHON_API,
    changeOrigin: true,
    pathRewrite: (p) => p.replace(/^\/api\/v1/, "/api"),
  })
);

// Health Node
app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "node-bridge", port: PORT, python: PYTHON_API });
});

// Static UI
app.use(express.static(path.join(__dirname, "public")));

app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, "127.0.0.1", () => {
  console.log(`[NODE] Mission Control → http://127.0.0.1:${PORT}`);
  console.log(`[NODE] Proxy API Python → ${PYTHON_API}`);
});
