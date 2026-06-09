#!/usr/bin/env node
/**
 * XMacro AI Guardian — analyse tout le projet Python,
 * détecte les erreurs, applique des corrections sûres.
 */

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const { applyFixes } = require("./fixer");

const COLORS = {
  reset: "\x1b[0m",
  green: "\x1b[92m",
  yellow: "\x1b[93m",
  red: "\x1b[91m",
  cyan: "\x1b[36m",
  magenta: "\x1b[95m",
};

function log(level, msg, extra = "") {
  const color =
    level === "OK" ? COLORS.green :
    level === "WARN" ? COLORS.yellow :
    level === "ERR" ? COLORS.red :
    level === "AI" ? COLORS.magenta : COLORS.cyan;
  const suffix = extra ? ` | ${extra}` : "";
  console.log(`${color}[AI-${level}]${COLORS.reset} ${msg}${suffix}`);
}

function resolveOnPath(cmd) {
  if (path.isAbsolute(cmd)) {
    return fs.existsSync(cmd) ? path.resolve(cmd) : null;
  }
  const pathEnv = process.env.PATH || process.env.Path || "";
  const sep = process.platform === "win32" ? ";" : ":";
  const ext = process.platform === "win32" ? ".exe" : "";
  for (const dir of pathEnv.split(sep)) {
    if (!dir) continue;
    for (const candidate of [path.join(dir, cmd + ext), path.join(dir, cmd)]) {
      if (fs.existsSync(candidate)) return path.resolve(candidate);
    }
  }
  return null;
}

function validateProjectRoot(projectRoot) {
  const resolved = path.resolve(projectRoot);
  if (!fs.existsSync(resolved) || !fs.statSync(resolved).isDirectory()) {
    throw new Error(`project_root invalide: ${projectRoot}`);
  }
  return resolved;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { project: process.cwd(), fix: false, watch: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--project" && args[i + 1]) {
      opts.project = validateProjectRoot(args[++i]);
    } else if (args[i] === "--fix") opts.fix = true;
    else if (args[i] === "--watch") opts.watch = true;
  }
  opts.project = validateProjectRoot(opts.project);
  return opts;
}

function walkDir(dir, exts, skip = []) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (skip.some((s) => full.includes(s))) continue;
      results.push(...walkDir(full, exts, skip));
    } else if (exts.some((e) => entry.name.endsWith(e))) {
      results.push(full);
    }
  }
  return results;
}

function checkMergeConflicts(content, file) {
  const issues = [];
  if (content.includes("<<<<<<<")) issues.push({ file, type: "merge_conflict", severity: "error" });
  return issues;
}

function checkPythonSyntax(file, pythonBin) {
  const safeFile = path.resolve(file);
  if (!safeFile.endsWith(".py") || !fs.existsSync(safeFile)) {
    return { file, type: "syntax_error", severity: "error", detail: "fichier Python invalide" };
  }
  const result = spawnSync(pythonBin, ["-m", "py_compile", safeFile], {
    stdio: "pipe",
    timeout: 10000,
  });
  if (result.status === 0) return null;
  const stderr = result.stderr ? result.stderr.toString() : result.error?.message || "py_compile failed";
  return { file, type: "syntax_error", severity: "error", detail: stderr.trim() };
}

function checkPatterns(content, file) {
  const issues = [];
  if (content.includes("setChecked") && content.includes("clicked.connect") && content.includes("burst")) {
    if (!content.includes("QButtonGroup") && !content.includes("blockSignals")) {
      issues.push({ file, type: "recursion_risk", severity: "warn", detail: "burst buttons sans QButtonGroup" });
    }
  }
  if (content.includes("sys.excepthook") && !content.includes("_handling_fatal")) {
    issues.push({ file, type: "excepthook_risk", severity: "warn", detail: "excepthook sans protection récursion" });
  }
  if (content.includes("while True:") && content.includes("_listener") && !content.includes("self.running")) {
    issues.push({ file, type: "listener_risk", severity: "warn", detail: "listener sans self.running" });
  }
  return issues;
}

function findPython() {
  const candidates = process.platform === "win32"
    ? ["python", "python3", "py"]
    : ["python3", "python"];
  for (const bin of candidates) {
    const resolved = resolveOnPath(bin);
    if (!resolved) continue;
    const result = spawnSync(resolved, ["--version"], { stdio: "pipe", timeout: 5000 });
    if (result.status === 0) return resolved;
  }
  return null;
}

function analyze(projectRoot, doFix) {
  projectRoot = validateProjectRoot(projectRoot);
  const pythonBin = findPython();
  if (!pythonBin) {
    log("ERR", "Python introuvable sur le PATH");
    return { issues: [], fixResults: [], ok: false };
  }
  log("AI", `Analyse du projet: ${projectRoot}`);
  const skip = [".git", "__pycache__", "node_modules", ".venv"];
  const pyFiles = walkDir(projectRoot, [".py"], skip);
  const jsonFiles = walkDir(projectRoot, [".json"], skip);
  const allFiles = [...pyFiles, ...jsonFiles];

  log("AI", `${allFiles.length} fichiers à analyser`);

  const issues = [];
  const fixable = [];

  for (const file of allFiles) {
    const rel = path.relative(projectRoot, file);
    let content = "";
    try {
      content = fs.readFileSync(file, "utf8");
    } catch (err) {
      issues.push({ file: rel, type: "read_error", severity: "error", detail: err.message });
      continue;
    }

    issues.push(...checkMergeConflicts(content, rel));
    issues.push(...checkPatterns(content, rel));

    if (content.includes("<<<<<<<")) fixable.push(rel);
    if (file.endsWith(".py")) {
      const syntaxErr = checkPythonSyntax(file, pythonBin);
      if (syntaxErr) issues.push({ ...syntaxErr, file: rel });
    }
  }

  let fixResults = [];
  if (doFix && fixable.length > 0) {
    log("AI", `Correction automatique sur ${fixable.length} fichier(s)...`);
    fixResults = applyFixes(projectRoot, fixable, false);
    for (const r of fixResults) {
      log("OK", `Corrigé: ${r.file}`, r.fixes.join(", "));
    }
    for (const file of fixable) {
      const full = path.join(projectRoot, file);
      const err = checkPythonSyntax(full, pythonBin);
      if (err) {
        issues.push({ ...err, file, type: "syntax_error_after_fix" });
      }
    }
  }

  const errors = issues.filter((i) => i.severity === "error");
  const warns = issues.filter((i) => i.severity === "warn");

  for (const i of errors) {
    log("ERR", `${i.file}: ${i.type}`, i.detail || "");
  }
  for (const i of warns) {
    log("WARN", `${i.file}: ${i.type}`, i.detail || "");
  }

  log("AI", `Résultat: ${errors.length} erreur(s), ${warns.length} avertissement(s), ${fixResults.length} correction(s)`);

  if (errors.length === 0) {
    log("OK", "Projet prêt — lancement XMacro autorisé");
  } else {
    log("ERR", "Erreurs détectées — vérifiez le terminal PyCharm");
  }

  return { issues, fixResults, ok: errors.length === 0 };
}

function main() {
  const opts = parseArgs();
  console.log(`${COLORS.magenta}╔══════════════════════════════════════╗${COLORS.reset}`);
  console.log(`${COLORS.magenta}║   XMacro AI Guardian (Node.js)       ║${COLORS.reset}`);
  console.log(`${COLORS.magenta}╚══════════════════════════════════════╝${COLORS.reset}`);

  const result = analyze(opts.project, opts.fix);

  if (opts.watch) {
    log("AI", "Mode watch actif (30s)...");
    setInterval(() => analyze(opts.project, opts.fix), 30000);
  } else {
    process.exit(result.ok ? 0 : 1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { analyze };
