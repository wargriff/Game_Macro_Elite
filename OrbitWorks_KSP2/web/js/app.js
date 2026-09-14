import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const state = {
  catalog: null,
  filtered: [],
  selected: null,
  tab: "all",
  autoRotate: true,
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

let renderer, scene, camera, controls, modelRoot, clock;

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

function clearModel() {
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

function buildStarship(g, craft) {
  const name = (craft.name || "").toLowerCase();
  const tall = name.includes("superheavy") || name.includes("full") || name.includes("deploy") || name.includes("stack");
  const stainless = 0xc9ced6;
  const dark = 0x2a2e36;

  if (tall) {
    // Super Heavy
    g.add(cyl(1.15, 1.22, 4.6, stainless, 2.3));
    for (let i = 0; i < 33; i++) {
      const a = (i / 33) * Math.PI * 2;
      const e = cyl(0.08, 0.12, 0.42, dark, 0.05, 12);
      e.position.set(Math.cos(a) * 0.95, 0.05, Math.sin(a) * 0.95);
      g.add(e);
    }
    // grid fins
    for (let i = 0; i < 4; i++) {
      const a = (i / 4) * Math.PI * 2 + 0.4;
      const fin = box(0.06, 0.7, 0.85, 0x8a909a, Math.cos(a) * 1.2, 3.8, Math.sin(a) * 1.2);
      g.add(fin);
    }
    // Ship
    g.add(cyl(1.05, 1.12, 3.8, stainless, 6.7));
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
    }
  } else {
    g.add(cyl(1.0, 1.08, 4.2, stainless, 2.1));
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
}

function buildSatellite(g, craft) {
  const starlink = craft.category === "starlink" || (craft.name || "").toLowerCase().includes("starlink");
  if (starlink) {
    const bus = box(1.55, 0.1, 0.55, 0x9aa3b0, 0, 0.35, 0, 0.65, 0.3);
    g.add(bus);
    const panel = box(2.4, 0.035, 0.7, 0x163a7a, 0, 0.35, 0);
    panel.material = mat(0x1a4a9a, 0.25, 0.35, 0x0a2858, 0.45);
    g.add(panel);
    const ph = box(0.35, 0.18, 0.25, 0xc8ccd4, 0.35, 0.5, 0);
    g.add(ph);
    const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.55, 8), mat(0xdddddd));
    ant.position.set(-0.45, 0.65, 0);
    g.add(ant);
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
  [[-0.55, -0.45], [-0.55, 0.45], [0.55, -0.45], [0.55, 0.45], [0, -0.55], [0, 0.55]].forEach(([x, z], i) => {
    if (i > 3) return;
    const w = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.2, 18), mat(0x222428, 0.15, 0.85));
    w.rotation.z = Math.PI / 2;
    w.position.set(x, 0.24, z);
    g.add(w);
  });
  g.add(cyl(0.045, 0.045, 0.9, 0xb0b4bc, 1.25));
  g.add(box(0.28, 0.14, 0.14, 0x333840, 0, 1.75, 0));
  const arm = box(0.08, 0.08, 0.7, 0x888c94, 0.55, 0.7, 0.2);
  g.add(arm);
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

function initScene() {
  const host = $("viewport");
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true;
  host.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x05080f, 0.016);

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

  // soft ground disc
  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(18, 64),
    new THREE.MeshStandardMaterial({ color: 0x0a121c, metalness: 0.1, roughness: 0.95 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  ground.receiveShadow = true;
  scene.add(ground);

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

function applyFilter() {
  const q = ($("q").value || "").trim().toLowerCase();
  const crafts = state.catalog.crafts || [];
  state.filtered = crafts.filter((c) => {
    if (q) {
      const hay = `${c.name} ${c.category} ${c.id} ${c.destination} ${(c.tags || []).join(" ")}`.toLowerCase();
      return hay.includes(q);
    }
    return state.tab === "all" || c.category === state.tab;
  });
  $("status").textContent = `${state.filtered.length} / ${crafts.length} appareils`;
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

  try {
    const fname = (c.blueprint_file || "").split("/").pop();
    const r = await fetch(`/export/Blueprints/${encodeURIComponent(fname)}`);
    $("blueprint-box").textContent = r.ok ? await r.text() : "Blueprint introuvable.";
  } catch {
    $("blueprint-box").textContent = "Erreur chargement blueprint.";
  }
}

async function loadCatalog() {
  const res = await fetch(`/web/catalog.json?t=${Date.now()}`);
  if (!res.ok) throw new Error("catalog.json manquant — lance generate_crafts.py");
  state.catalog = await res.json();
  renderTabs();
  applyFilter();
  if (state.filtered[0]) selectCraft(state.filtered[0]);
}

function bindUi() {
  $("q").addEventListener("input", applyFilter);
  $("btn-blueprint").addEventListener("click", () => {
    $("blueprint-box").classList.toggle("hidden");
  });
  $("btn-rotate").addEventListener("click", () => {
    state.autoRotate = !state.autoRotate;
    $("btn-rotate").textContent = state.autoRotate ? "Auto-rotate ON" : "Auto-rotate OFF";
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
