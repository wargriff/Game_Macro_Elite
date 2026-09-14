import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const state = {
  catalog: null,
  filtered: [],
  selected: null,
  tab: "all",
  destination: "all",
  sort: "name",
  autoRotate: true,
  wireframe: false,
};

const TAB_ORDER = ["all", "starlink", "starship", "rockets", "rovers", "comms", "data"];
const TAB_LABELS = {
  all: "Tous",
  starlink: "Starlink",
  starship: "Starship",
  rockets: "Fusées",
  rovers: "Rovers",
  comms: "Comms",
  data: "Data",
};

let renderer, scene, camera, controls, modelRoot, clock, starField, engineLights = [];

const $ = (id) => document.getElementById(id);

function mat(color, metal = 0.55, rough = 0.38, emissive = 0x000000, em = 0) {
  return new THREE.MeshStandardMaterial({
    color,
    metalness: metal,
    roughness: rough,
    emissive,
    emissiveIntensity: em,
  });
}

function cyl(rTop, rBot, h, color, y, segs = 32) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rTop, rBot, h, segs), mat(color));
  m.position.y = y;
  m.castShadow = true;
  m.receiveShadow = true;
  return m;
}

function box(w, h, d, color, x, y, z, metal = 0.4, rough = 0.45) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(color, metal, rough));
  m.position.set(x, y, z);
  m.castShadow = true;
  return m;
}

function addEngineGlow(parent, x, y, z, scale = 1) {
  const glow = new THREE.Mesh(
    new THREE.ConeGeometry(0.18 * scale, 0.55 * scale, 16, 1, true),
    mat(0xffaa55, 0.1, 0.4, 0xff6600, 1.4)
  );
  glow.position.set(x, y, z);
  glow.rotation.x = Math.PI;
  parent.add(glow);
  engineLights.push(glow);
  return glow;
}

function clearModel() {
  engineLights = [];
  while (modelRoot.children.length) {
    const obj = modelRoot.children[0];
    modelRoot.remove(obj);
    obj.traverse((c) => {
      if (c.geometry) c.geometry.dispose();
      if (c.material) {
        if (Array.isArray(c.material)) c.material.forEach((m) => m.dispose());
        else c.material.dispose();
      }
    });
  }
}

function applyWireframe(enabled) {
  modelRoot.traverse((c) => {
    if (c.isMesh && c.material) {
      if (Array.isArray(c.material)) c.material.forEach((m) => (m.wireframe = enabled));
      else c.material.wireframe = enabled;
    }
  });
}

function buildStarship(g, craft) {
  const name = (craft.name || "").toLowerCase();
  const tall =
    name.includes("superheavy") ||
    name.includes("full") ||
    name.includes("deploy") ||
    name.includes("stack") ||
    name.includes("crew") ||
    name.includes("cargo") ||
    name.includes("tanker") ||
    name.includes("hls") ||
    name.includes("depot") ||
    name.includes("transport");
  const stainless = 0xc9ced6;
  const dark = 0x2a2e36;
  const tile = 0x3a342e;

  if (tall) {
    g.add(cyl(1.15, 1.22, 4.6, stainless, 2.3));
    // heat-tile band
    g.add(cyl(1.16, 1.16, 0.35, tile, 3.8));
    for (let i = 0; i < 33; i++) {
      const a = (i / 33) * Math.PI * 2;
      const e = cyl(0.08, 0.12, 0.42, dark, 0.05, 12);
      e.position.set(Math.cos(a) * 0.95, 0.05, Math.sin(a) * 0.95);
      g.add(e);
      if (i % 3 === 0) addEngineGlow(g, Math.cos(a) * 0.95, -0.25, Math.sin(a) * 0.95, 0.7);
    }
    for (let i = 0; i < 4; i++) {
      const a = (i / 4) * Math.PI * 2 + 0.4;
      g.add(box(0.06, 0.7, 0.85, 0x8a909a, Math.cos(a) * 1.2, 3.8, Math.sin(a) * 1.2));
    }
    g.add(cyl(1.05, 1.12, 3.8, stainless, 6.7));
    g.add(cyl(1.06, 1.06, 0.25, tile, 5.2));
    const nose = new THREE.Mesh(new THREE.ConeGeometry(1.05, 1.9, 32), mat(0xd7dde6, 0.75, 0.22));
    nose.position.y = 9.55;
    g.add(nose);
    [-1, 1].forEach((s, idx) => {
      const flap = box(0.1, 1.5, 1.55, 0xa8aeb8, s * 1.1, 7.4, idx ? 0.15 : -0.15);
      flap.rotation.z = s * 0.18;
      g.add(flap);
    });
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      const e = cyl(0.12, 0.18, 0.5, dark, 4.55, 12);
      e.position.set(Math.cos(a) * 0.7, 4.55, Math.sin(a) * 0.7);
      g.add(e);
      addEngineGlow(g, Math.cos(a) * 0.7, 4.2, Math.sin(a) * 0.7, 0.85);
    }
  } else {
    g.add(cyl(1.0, 1.08, 4.2, stainless, 2.1));
    g.add(cyl(1.01, 1.01, 0.28, tile, 1.0));
    const nose = new THREE.Mesh(new THREE.ConeGeometry(1.0, 1.7, 32), mat(0xd7dde6, 0.75, 0.22));
    nose.position.y = 5.05;
    g.add(nose);
    [-1, 1].forEach((s) => {
      const flap = box(0.1, 1.35, 1.35, 0xa8aeb8, s * 1.05, 2.9, 0);
      flap.rotation.z = s * 0.16;
      g.add(flap);
    });
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      const e = cyl(0.14, 0.2, 0.55, dark, 0.05, 12);
      e.position.set(Math.cos(a) * 0.72, 0.05, Math.sin(a) * 0.72);
      g.add(e);
      addEngineGlow(g, Math.cos(a) * 0.72, -0.35, Math.sin(a) * 0.72, 0.9);
    }
  }
}

function buildRocket(g, craft) {
  const stages = Math.max(2, Math.min(5, Math.round((craft.parts_count || 12) / 10)));
  let y = 0;
  const palette = [0xe8e2d6, 0xd4a574, 0xe8e2d6, 0xc0c4cc];
  for (let i = 0; i < stages; i++) {
    const h = 1.35 + (stages - i) * 0.28;
    const r = 0.58 - i * 0.05;
    g.add(cyl(r, r + 0.05, h, palette[i % palette.length], y + h / 2));
    // rivet ring
    g.add(cyl(r + 0.02, r + 0.02, 0.06, 0x8890a0, y + h * 0.35));
    if (i < stages - 1) {
      g.add(cyl(r * 0.92, r * 0.92, 0.12, 0x333840, y + h + 0.06));
    }
    y += h + (i < stages - 1 ? 0.12 : 0);
  }
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.45, 1.15, 24), mat(0xf2eee6, 0.45, 0.32));
  nose.position.y = y + 0.55;
  g.add(nose);
  for (let i = 0; i < 4; i++) {
    const a = (i / 4) * Math.PI * 2;
    g.add(box(0.06, 0.75, 0.48, 0xb0a090, Math.cos(a) * 0.58, 0.42, Math.sin(a) * 0.58));
  }
  g.add(cyl(0.24, 0.34, 0.5, 0x333840, -0.18));
  addEngineGlow(g, 0, -0.55, 0, 1.1);
}

function buildSatellite(g, craft) {
  const starlink = craft.category === "starlink" || (craft.name || "").toLowerCase().includes("starlink");
  if (starlink) {
    g.add(box(1.55, 0.1, 0.55, 0x9aa3b0, 0, 0.35, 0, 0.65, 0.3));
    const panel = box(2.4, 0.035, 0.7, 0x163a7a, 0, 0.35, 0);
    panel.material = mat(0x1a4a9a, 0.25, 0.35, 0x0a2858, 0.45);
    g.add(panel);
    // cell lines
    for (let i = -2; i <= 2; i++) {
      g.add(box(0.02, 0.04, 0.68, 0x0d2a5a, i * 0.4, 0.37, 0));
    }
    g.add(box(0.35, 0.18, 0.25, 0xc8ccd4, 0.35, 0.5, 0));
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.55, 8), mat(0xdddddd));
    ant.position.set(-0.45, 0.65, 0);
    g.add(ant);
    const tip = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 12), mat(0xffcc66, 0.2, 0.3, 0xffaa33, 0.8));
    tip.position.set(-0.45, 0.95, 0);
    g.add(tip);
  } else {
    g.add(box(0.95, 0.4, 0.75, 0xc4c8d0, 0, 0.45, 0));
    const dish = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.05, 32), mat(0xffffff, 0.9, 0.12));
    dish.rotation.x = Math.PI / 2;
    dish.position.set(0, 0.75, 0);
    g.add(dish);
    [-1, 1].forEach((s) => {
      const panel = box(1.7, 0.04, 0.55, 0x1a3a6a, s * 1.4, 0.45, 0);
      panel.material = mat(0x1a4080, 0.3, 0.4, 0x0a2040, 0.4);
      g.add(panel);
    });
  }
}

function buildRover(g) {
  g.add(box(1.55, 0.38, 1.0, 0xc4a574, 0, 0.48, 0));
  g.add(box(0.55, 0.42, 0.55, 0x8890a0, 0, 0.9, 0));
  [[-0.55, -0.45], [-0.55, 0.45], [0.55, -0.45], [0.55, 0.45]].forEach(([x, z]) => {
    const w = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.2, 18), mat(0x222428, 0.15, 0.85));
    w.rotation.z = Math.PI / 2;
    w.position.set(x, 0.24, z);
    g.add(w);
  });
  g.add(cyl(0.045, 0.045, 0.9, 0xb0b4bc, 1.25));
  g.add(box(0.28, 0.14, 0.14, 0x333840, 0, 1.75, 0));
  g.add(box(0.08, 0.08, 0.7, 0x888c94, 0.55, 0.7, 0.2));
  const cam = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 12), mat(0x111318, 0.7, 0.2, 0x3388ff, 0.5));
  cam.position.set(0, 1.75, 0.12);
  g.add(cam);
}

function buildCraft(craft) {
  clearModel();
  const g = new THREE.Group();
  const cat = craft.category || "";
  const preview = craft.preview || cat;
  if (cat === "starship" || preview === "starship") buildStarship(g, craft);
  else if (cat === "starlink" || cat === "comms" || cat === "data" || preview === "starlink") buildSatellite(g, craft);
  else if (cat === "rovers") buildRover(g);
  else buildRocket(g, craft);
  modelRoot.add(g);
  applyWireframe(state.wireframe);
  fitCamera(g);
}

function fitCamera(g) {
  const box3 = new THREE.Box3().setFromObject(g);
  const size = box3.getSize(new THREE.Vector3());
  const center = box3.getCenter(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z, 1);
  const dist = maxDim * 2.35;
  controls.target.copy(center);
  camera.position.set(center.x + dist * 0.75, center.y + dist * 0.38, center.z + dist * 0.95);
  controls.update();
}

function makeStars() {
  const n = 1200;
  const positions = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const r = 40 + Math.random() * 80;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const points = new THREE.Points(
    geo,
    new THREE.PointsMaterial({ color: 0xb8d4ff, size: 0.12, sizeAttenuation: true, transparent: true, opacity: 0.85 })
  );
  return points;
}

function initScene() {
  const host = $("viewport");
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true;
  host.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x05080f, 0.012);

  camera = new THREE.PerspectiveCamera(42, 1, 0.1, 500);
  camera.position.set(8, 4.5, 10);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.target.set(0, 1.4, 0);

  scene.add(new THREE.HemisphereLight(0xb8d4ff, 0x1a1408, 0.9));
  const key = new THREE.DirectionalLight(0xfff2dd, 1.2);
  key.position.set(9, 16, 7);
  key.castShadow = true;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x4db8ff, 0.5);
  rim.position.set(-12, 5, -9);
  scene.add(rim);

  const grid = new THREE.GridHelper(48, 48, 0x1e3a4a, 0x101820);
  grid.position.y = -0.01;
  scene.add(grid);

  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(18, 64),
    new THREE.MeshStandardMaterial({ color: 0x0a121c, metalness: 0.1, roughness: 0.95 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  ground.receiveShadow = true;
  scene.add(ground);

  starField = makeStars();
  scene.add(starField);

  modelRoot = new THREE.Group();
  scene.add(modelRoot);
  clock = new THREE.Clock();
  onResize();
  window.addEventListener("resize", onResize);
}

function onResize() {
  const host = $("viewport");
  const w = host.clientWidth || 800;
  const h = host.clientHeight || 600;
  renderer.setSize(w, h, false);
  camera.aspect = w / Math.max(h, 1);
  camera.updateProjectionMatrix();
}

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  if (state.autoRotate && modelRoot.children[0]) {
    modelRoot.children[0].rotation.y = t * 0.28;
  }
  engineLights.forEach((e, i) => {
    const pulse = 0.9 + Math.sin(t * 8 + i) * 0.35;
    if (e.material) e.material.emissiveIntensity = pulse;
    e.scale.setScalar(0.85 + Math.sin(t * 10 + i * 0.7) * 0.2);
  });
  if (starField) starField.rotation.y = t * 0.01;
  controls.update();
  renderer.render(scene, camera);
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderTabs() {
  const tabs = $("tabs");
  tabs.innerHTML = "";
  const present = new Set((state.catalog.crafts || []).map((c) => c.category));
  TAB_ORDER.filter((t) => t === "all" || present.has(t)).forEach((id) => {
    const btn = document.createElement("button");
    btn.className = "tab" + (state.tab === id ? " active" : "");
    btn.textContent = TAB_LABELS[id] || id;
    btn.addEventListener("click", () => {
      state.tab = id;
      renderTabs();
      applyFilter();
    });
    tabs.appendChild(btn);
  });
}

function renderChips() {
  const chips = $("chips");
  chips.innerHTML = "";
  const dests = ["all", ...new Set((state.catalog.crafts || []).map((c) => c.destination).filter(Boolean))].slice(0, 14);
  dests.forEach((d) => {
    const btn = document.createElement("button");
    btn.className = "chip" + (state.destination === d ? " active" : "");
    btn.textContent = d === "all" ? "Toutes dest." : d;
    btn.addEventListener("click", () => {
      state.destination = d;
      renderChips();
      applyFilter();
    });
    chips.appendChild(btn);
  });
}

function sortCrafts(list) {
  const arr = [...list];
  switch (state.sort) {
    case "mass":
      arr.sort((a, b) => (b.mass_t || 0) - (a.mass_t || 0));
      break;
    case "dv":
      arr.sort((a, b) => (b.estimated_dv_ms || 0) - (a.estimated_dv_ms || 0));
      break;
    case "parts":
      arr.sort((a, b) => (b.parts_count || 0) - (a.parts_count || 0));
      break;
    default:
      arr.sort((a, b) => String(a.name).localeCompare(String(b.name), "fr"));
  }
  return arr;
}

function applyFilter() {
  const q = ($("q").value || "").trim().toLowerCase();
  const crafts = state.catalog.crafts || [];
  let filtered = crafts.filter((c) => {
    if (state.tab !== "all" && c.category !== state.tab) return false;
    if (state.destination !== "all" && c.destination !== state.destination) return false;
    if (q) {
      const hay = `${c.name} ${c.category} ${c.id} ${c.destination} ${(c.tags || []).join(" ")}`.toLowerCase();
      return hay.includes(q);
    }
    return true;
  });
  filtered = sortCrafts(filtered);
  state.filtered = filtered;
  $("status").textContent = `${filtered.length} / ${crafts.length} appareils`;
  renderList();
}

function renderList() {
  const list = $("list");
  list.innerHTML = "";
  state.filtered.forEach((c) => {
    const el = document.createElement("div");
    el.className = "item" + (state.selected?.id === c.id ? " active" : "");
    el.innerHTML = `
      <h3>${escapeHtml(c.name)}</h3>
      <div class="meta">
        <span class="badge">${escapeHtml(c.category)}</span>
        <span class="badge a">${c.parts_count} pcs</span>
        <span class="badge g">${Number(c.mass_t).toFixed(1)} t</span>
      </div>`;
    el.addEventListener("click", () => selectCraft(c));
    list.appendChild(el);
  });
}

function renderPartsTable(c) {
  const host = $("parts-table");
  const parts = c.parts || [];
  if (!parts.length) {
    host.innerHTML = `<div class="part-row"><span></span><span>Aucune pièce listée</span><span></span></div>`;
    return;
  }
  host.innerHTML = parts
    .map(
      (p) => `
      <div class="part-row">
        <span class="qty">×${p.qty}</span>
        <span>${escapeHtml(p.display_name || p.part_id)}</span>
        <span class="role">${escapeHtml(p.role || p.category || "")}</span>
      </div>`
    )
    .join("");
}

async function selectCraft(c) {
  state.selected = c;
  renderList();
  buildCraft(c);
  $("hud-title").textContent = c.name;
  $("hud-sub").textContent = `${c.destination || "—"} · ${c.subtype || c.type || c.category} · Δv ~ ${c.estimated_dv_ms} m/s`;
  $("hud-stats").innerHTML = `
    <div class="stat"><b>Pièces</b>${c.parts_count}</div>
    <div class="stat"><b>Masse</b>${Number(c.mass_t).toFixed(2)} t</div>
    <div class="stat"><b>Δv</b>${c.estimated_dv_ms} m/s</div>
    <div class="stat"><b>Cat.</b>${escapeHtml(c.category)}</div>`;
  renderPartsTable(c);

  try {
    const fname = (c.blueprint_file || "").split("/").pop();
    const r = await fetch(`/export/Blueprints/${encodeURIComponent(fname)}`);
    $("blueprint-box").textContent = r.ok ? await r.text() : "Blueprint introuvable.";
  } catch {
    $("blueprint-box").textContent = "Erreur chargement blueprint.";
  }
}

function stepCraft(delta) {
  if (!state.filtered.length) return;
  const idx = Math.max(0, state.filtered.findIndex((c) => c.id === state.selected?.id));
  const next = state.filtered[(idx + delta + state.filtered.length) % state.filtered.length];
  selectCraft(next);
}

function checklistText(c) {
  const lines = [`# ${c.name}`, `Destination: ${c.destination || "—"}`, "", "Checklist VAB:"];
  (c.parts || []).forEach((p) => {
    lines.push(`- [ ] ×${p.qty}  ${p.display_name || p.part_id}`);
  });
  return lines.join("\n");
}

async function loadCatalog() {
  const res = await fetch(`/web/catalog.json?t=${Date.now()}`);
  if (!res.ok) throw new Error("catalog.json manquant — lance generate_crafts.py");
  state.catalog = await res.json();
  renderTabs();
  renderChips();
  applyFilter();
  if (state.filtered[0]) selectCraft(state.filtered[0]);
}

function bindUi() {
  $("q").addEventListener("input", applyFilter);
  $("sort").addEventListener("change", () => {
    state.sort = $("sort").value;
    applyFilter();
  });
  $("btn-prev").addEventListener("click", () => stepCraft(-1));
  $("btn-next").addEventListener("click", () => stepCraft(1));
  $("btn-blueprint").addEventListener("click", () => {
    $("blueprint-box").classList.toggle("hidden");
  });
  $("btn-copy").addEventListener("click", async () => {
    if (!state.selected) return;
    const text = checklistText(state.selected);
    try {
      await navigator.clipboard.writeText(text);
      $("btn-copy").textContent = "Copié ✓";
      setTimeout(() => ($("btn-copy").textContent = "Copier checklist"), 1200);
    } catch {
      $("blueprint-box").classList.remove("hidden");
      $("blueprint-box").textContent = text;
    }
  });
  $("btn-rotate").addEventListener("click", () => {
    state.autoRotate = !state.autoRotate;
    $("btn-rotate").textContent = state.autoRotate ? "Auto-rotate ON" : "Auto-rotate OFF";
  });
  $("btn-wire").addEventListener("click", () => {
    state.wireframe = !state.wireframe;
    applyWireframe(state.wireframe);
    $("btn-wire").textContent = state.wireframe ? "Wireframe ON" : "Wireframe";
  });
  $("btn-reset").addEventListener("click", () => {
    if (state.selected) buildCraft(state.selected);
  });
  window.addEventListener("keydown", (e) => {
    if (e.target && ["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
    if (e.key === "ArrowLeft") stepCraft(-1);
    if (e.key === "ArrowRight") stepCraft(1);
    if (e.key === "w") $("btn-wire").click();
    if (e.key === "r") $("btn-rotate").click();
  });
  $("btn-rotate").textContent = "Auto-rotate ON";
}

async function boot() {
  initScene();
  bindUi();
  await loadCatalog();
  animate();
}

boot().catch((err) => {
  console.error(err);
  $("status").textContent = "Erreur: " + err.message;
});
