const fs = require("fs");
const path = require("path");

const MERGE_START = /^<<<<<<< /;
const MERGE_SEP = /^=======\s*$/;
const MERGE_END = /^>>>>>>> /;

function fixMergeConflicts(content) {
  const lines = content.split("\n");
  const out = [];
  let inConflict = false;
  let takeHead = true;
  let fixed = false;

  for (const line of lines) {
    if (MERGE_START.test(line)) {
      inConflict = true;
      takeHead = true;
      fixed = true;
      continue;
    }
    if (inConflict && MERGE_SEP.test(line)) {
      takeHead = false;
      continue;
    }
    if (inConflict && MERGE_END.test(line)) {
      inConflict = false;
      continue;
    }
    if (!inConflict || takeHead) {
      out.push(line);
    }
  }
  return { content: out.join("\n"), fixed };
}

function fixTrailingWhitespace(content) {
  const lines = content.split("\n");
  let fixed = false;
  const cleaned = lines.map((line) => {
    const trimmed = line.replace(/\s+$/, "");
    if (trimmed !== line) fixed = true;
    return trimmed;
  });
  return { content: cleaned.join("\n"), fixed };
}

function fixMissingFinalNewline(content) {
  if (content.length > 0 && !content.endsWith("\n")) {
    return { content: content + "\n", fixed: true };
  }
  return { content, fixed: false };
}

function fixFile(filePath, dryRun = false) {
  const fixes = [];
  let content = fs.readFileSync(filePath, "utf8");
  let changed = false;

  const steps = [fixMergeConflicts, fixTrailingWhitespace, fixMissingFinalNewline];
  for (const step of steps) {
    const result = step(content);
    if (result.fixed) {
      fixes.push(step.name);
      content = result.content;
      changed = true;
    }
  }

  if (changed && !dryRun) {
    fs.writeFileSync(filePath, content, "utf8");
  }

  return { changed, fixes };
}

function applyFixes(projectRoot, files, dryRun = false) {
  const results = [];
  for (const rel of files) {
    const full = path.join(projectRoot, rel);
    if (!fs.existsSync(full)) continue;
    try {
      const { changed, fixes } = fixFile(full, dryRun);
      if (changed) {
        results.push({ file: rel, fixes, applied: !dryRun });
      }
    } catch (err) {
      results.push({ file: rel, error: err.message });
    }
  }
  return results;
}

module.exports = { fixFile, applyFixes, fixMergeConflicts };
