/* ==========================================================================
   智高 T082R 等臂天平 3D 互動主控程式
   支援：360° 視角控制、6 步驟拆解動畫、爆炸檢視、點擊查官方品號、
         教案第 2～3 節放物與紅方塊加減平衡動態物理模擬、BOM 互動高亮
   ========================================================================== */

(function () {
  "use strict";

  // 教案課堂實物清單（涵蓋三年級文具輕物至教師示範 500g–1kg 重物）
  const TEST_ITEMS = [
    { id: "none", name: "（空盤）", grams: 0, color: 0x94a3b8, size: [0, 0, 0] },
    { id: "eraser", name: "大橡皮擦（約 24g）", grams: 24, color: 0xf8fafc, size: [2.6, 1.1, 4.2] },
    { id: "glue", name: "膠水一瓶（約 54g）", grams: 54, color: 0x38bdf8, size: [2.4, 4.6, 2.4] },
    { id: "pencilcase", name: "鉛筆盒（約 180g）", grams: 180, color: 0x6366f1, size: [7.6, 2.2, 3.6] },
    { id: "book", name: "三年級數學課本（約 500g）", grams: 500, color: 0xf59e0b, size: [8.4, 1.8, 8.4] },
    { id: "rice", name: "1 公斤白米示範包（1000g）", grams: 1000, color: 0x10b981, size: [7.4, 4.4, 7.4] }
  ];

  const UNIT_GRAMS = 3; // 單顆紅 C-20T 齒輪換算示範克數
  const MAX_WEIGHT_UNITS = 20; // 兩盒 #1248R-CN 共含 20 顆紅 C-20T 齒輪

  const state = {
    mode: "assembly", // assembly | simulate | bom
    step: 6,
    explode: 0,
    theme: "light",
    highlightedType: null,
    selectedPart: null,
    sim: {
      leftItem: "none",
      rightItem: "none",
      leftCubes: 0,
      rightCubes: 0,
      angle: 0,
      angVel: 0,
      targetAngle: 0
    }
  };

  // DOM 參照
  const container = document.getElementById("canvas-container");
  const tabBtns = document.querySelectorAll(".tab-btn");
  const views = {
    assembly: document.getElementById("view-assembly"),
    simulate: document.getElementById("view-simulate"),
    bom: document.getElementById("view-bom")
  };
  const stepBadge = document.getElementById("step-badge");
  const stepTitle = document.getElementById("step-title");
  const stepDesc = document.getElementById("step-desc");
  const stepPartsList = document.getElementById("step-parts-list");
  const stepTipsList = document.getElementById("step-tips-list");
  const stepDots = document.getElementById("step-dots");
  const btnPrev = document.getElementById("btn-prev-step");
  const btnNext = document.getElementById("btn-next-step");
  const explodeSlider = document.getElementById("explode-slider");
  const explodeVal = document.getElementById("explode-val");
  const explodeControl = document.getElementById("explode-control");
  const btnTheme = document.getElementById("btn-theme");

  const inspectorCard = document.getElementById("inspector-card");
  const inspSwatch = document.getElementById("insp-swatch");
  const inspCode = document.getElementById("insp-code");
  const inspName = document.getElementById("insp-name");
  const inspSpec = document.getElementById("insp-spec");
  const inspStep = document.getElementById("insp-step");
  const inspRole = document.getElementById("insp-role");
  const inspClose = document.getElementById("insp-close");

  // 模擬模式 DOM
  const leftSelect = document.getElementById("left-item-select");
  const rightSelect = document.getElementById("right-item-select");
  const leftCubeCount = document.getElementById("left-cube-count");
  const rightCubeCount = document.getElementById("right-cube-count");
  const leftTotalEl = document.getElementById("left-total");
  const rightTotalEl = document.getElementById("right-total");
  const readoutBox = document.getElementById("balance-readout");
  const readoutStatus = document.getElementById("readout-status");

  // ------------------------------------------------------------------------
  // Three.js 場景初始化
  // ------------------------------------------------------------------------
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xe2e8f0);

  const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.5, 400);
  camera.position.set(28, 26, 36);

  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 10, 0);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 12;
  controls.maxDistance = 95;
  controls.maxPolarAngle = Math.PI * 0.49;

  // 棚拍三點光源
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x94a3b8, 0.85);
  scene.add(hemiLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
  dirLight.position.set(24, 42, 26);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.set(2048, 2048);
  dirLight.shadow.camera.near = 5;
  dirLight.shadow.camera.far = 120;
  const d = 28;
  dirLight.shadow.camera.left = -d;
  dirLight.shadow.camera.right = d;
  dirLight.shadow.camera.top = d;
  dirLight.shadow.camera.bottom = -d;
  dirLight.shadow.bias = -0.0005;
  scene.add(dirLight);

  const fillLight = new THREE.DirectionalLight(0xbae6fd, 0.35);
  fillLight.position.set(-22, 16, -20);
  scene.add(fillLight);

  // 工作檯面與 10mm 格線（1 格 = 智高 1 孔距 10mm）
  const floorGeo = new THREE.PlaneGeometry(140, 140);
  const floorMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.92, metalness: 0.0 });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  const gridHelper = new THREE.GridHelper(60, 60, 0x94a3b8, 0xcbd5e1);
  gridHelper.position.y = 0.02;
  scene.add(gridHelper);

  // 載入智高 T082R 等臂天平實體模型
  const assembly = window.buildGigoBalanceAssembly();
  scene.add(assembly.rootGroup);

  // 左右托盤動態物品群組（置於防漏格柵底板頂面 Y = 2.62，中心精準對齊 ±10.5）
  const leftPanLoadGroup = new THREE.Group();
  leftPanLoadGroup.position.set(-10.5, 2.62, 0);
  const rightPanLoadGroup = new THREE.Group();
  rightPanLoadGroup.position.set(10.5, 2.62, 0);
  assembly.pivotGroup.add(leftPanLoadGroup, rightPanLoadGroup);

  // 高亮線框輔助器
  const highlightBoxes = new THREE.Group();
  scene.add(highlightBoxes);

  function clearHighlights() {
    while (highlightBoxes.children.length > 0) {
      const c = highlightBoxes.children.pop();
      if (c.geometry) c.geometry.dispose();
      if (c.material) c.material.dispose();
    }
  }

  function highlightParts(predicate) {
    clearHighlights();
    if (!predicate) return;
    assembly.allParts.forEach((p) => {
      if (p.mesh.visible && predicate(p)) {
        const helper = new THREE.BoxHelper(p.mesh, 0x2563eb);
        highlightBoxes.add(helper);
      }
    });
  }

  // ------------------------------------------------------------------------
  // 視角動畫
  // ------------------------------------------------------------------------
  let camAnim = null;
  const CAM_PRESETS = {
    iso: { pos: [28, 25, 36], target: [0, 10, 0] },
    front: { pos: [0, 13, 44], target: [0, 10, 0] },
    side: { pos: [40, 14, 2], target: [0, 12, 0] },
    top: { pos: [0, 48, 8], target: [0, 10, 0] }
  };

  function moveCamera(presetKey) {
    const p = CAM_PRESETS[presetKey];
    if (!p) return;
    camAnim = {
      startPos: camera.position.clone(),
      endPos: new THREE.Vector3(...p.pos),
      startTarget: controls.target.clone(),
      endTarget: new THREE.Vector3(...p.target),
      t: 0
    };
  }

  document.querySelectorAll("[data-cam]").forEach((btn) => {
    btn.addEventListener("click", () => moveCamera(btn.dataset.cam));
  });

  // ------------------------------------------------------------------------
  // 步驟更新與 UI 同步
  // ------------------------------------------------------------------------
  function initStepDots() {
    stepDots.innerHTML = "";
    window.ASSEMBLY_STEPS.forEach((s) => {
      const btn = document.createElement("button");
      btn.className = "step-dot";
      btn.textContent = `S${s.step}`;
      btn.setAttribute("role", "tab");
      btn.addEventListener("click", () => setStep(s.step));
      stepDots.appendChild(btn);
    });
  }

  function setStep(stepNum) {
    state.step = Math.max(1, Math.min(6, stepNum));
    const info = window.ASSEMBLY_STEPS[state.step - 1];
    stepBadge.textContent = `步驟 ${state.step} / 6`;
    stepTitle.textContent = info.title;
    stepDesc.textContent = info.desc;

    btnPrev.disabled = state.step <= 1;
    btnNext.disabled = state.step >= 6;

    stepDots.querySelectorAll(".step-dot").forEach((el, idx) => {
      el.classList.toggle("active", idx + 1 === state.step);
    });

    // 統計本步驟使用零件
    const counts = new Map();
    assembly.allParts.forEach((p) => {
      if (p.step === state.step) {
        counts.set(p.typeKey, (counts.get(p.typeKey) || 0) + 1);
      }
      p.mesh.visible = state.mode === "assembly" ? p.step <= state.step : true;
    });

    stepPartsList.innerHTML = "";
    counts.forEach((qty, typeKey) => {
      const cat = window.GIGO_CATALOG[typeKey];
      const li = document.createElement("li");
      li.className = "step-part-item";
      li.innerHTML = `
        <div class="step-part-left">
          <span class="part-swatch" style="background:${cat.swatch}"></span>
          <div>
            <span class="step-part-name">${cat.name}</span>
            <span class="step-part-code">${cat.code}</span>
          </div>
        </div>
        <span class="qty-badge">× ${qty}</span>
      `;
      li.addEventListener("click", () => {
        highlightParts((p) => p.typeKey === typeKey && p.step === state.step);
      });
      stepPartsList.appendChild(li);
    });

    stepTipsList.innerHTML = info.tips.map((t) => `<li>${t}</li>`).join("");
    clearHighlights();
  }

  btnPrev.addEventListener("click", () => setStep(state.step - 1));
  btnNext.addEventListener("click", () => setStep(state.step + 1));

  // 爆炸拆解滑桿
  explodeSlider.addEventListener("input", (e) => {
    state.explode = Number(e.target.value) / 100;
    explodeVal.textContent = `${e.target.value}%`;
  });

  // ------------------------------------------------------------------------
  // BOM 表自動由 3D 實體模型彙整（保證 100% 一致）
  // ------------------------------------------------------------------------
  function renderBOM() {
    const counts = new Map();
    assembly.allParts.forEach((p) => {
      counts.set(p.typeKey, (counts.get(p.typeKey) || 0) + 1);
    });

    let structTotal = 0;
    let weightTotal = 0;
    const tbody = document.getElementById("bom-tbody");
    tbody.innerHTML = "";

    Object.keys(window.GIGO_CATALOG).forEach((key) => {
      const qty = counts.get(key) || 0;
      if (qty === 0) return;
      const cat = window.GIGO_CATALOG[key];
      if (cat.category === "weight") weightTotal += qty;
      else structTotal += qty;

      const tr = document.createElement("tr");
      if (cat.category === "weight") tr.className = "is-weight-row";
      tr.innerHTML = `
        <td>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="part-swatch" style="background:${cat.swatch};width:14px;height:14px;border-radius:4px;"></span>
            <div>
              <div style="font-weight:700">${cat.name}</div>
              <div style="font-size:11.5px;color:var(--text-muted);font-family:monospace">${cat.code} · ${cat.spec}</div>
            </div>
          </div>
        </td>
        <td style="font-size:12px;color:var(--text-secondary)">${cat.usage}</td>
        <td class="num">${qty} <span style="font-size:11px;font-weight:600;color:var(--text-muted)">/ ${cat.maxQty2Boxes}</span></td>
      `;
      tr.addEventListener("click", () => {
        highlightParts((p) => p.typeKey === key);
      });
      tbody.appendChild(tr);
    });

    document.getElementById("bom-struct-total").textContent = structTotal;
    document.getElementById("bom-weight-total").textContent = weightTotal;
    document.getElementById("bom-types-total").textContent = counts.size;
  }

  // ------------------------------------------------------------------------
  // 測重與紅方塊加減平衡模擬
  // ------------------------------------------------------------------------
  function initSimSelects() {
    const html = TEST_ITEMS.map((item) => `<option value="${item.id}">${item.name}</option>`).join("");
    leftSelect.innerHTML = html;
    rightSelect.innerHTML = html;

    leftSelect.addEventListener("change", () => {
      state.sim.leftItem = leftSelect.value;
      updateSimVisuals();
    });
    rightSelect.addEventListener("change", () => {
      state.sim.rightItem = rightSelect.value;
      updateSimVisuals();
    });

    document.getElementById("left-cube-plus").addEventListener("click", () => adjustCubes("left", 1));
    document.getElementById("left-cube-minus").addEventListener("click", () => adjustCubes("left", -1));
    document.getElementById("right-cube-plus").addEventListener("click", () => adjustCubes("right", 1));
    document.getElementById("right-cube-minus").addEventListener("click", () => adjustCubes("right", -1));

    document.getElementById("btn-sim-preset").addEventListener("click", () => {
      state.sim.leftItem = "eraser";
      state.sim.rightItem = "none";
      state.sim.leftCubes = 0;
      state.sim.rightCubes = 8; // 8 顆 × 3g = 24g 剛好平衡大橡皮擦！
      leftSelect.value = "eraser";
      rightSelect.value = "none";
      updateSimVisuals();
    });

    document.getElementById("btn-sim-reset").addEventListener("click", () => {
      state.sim.leftItem = "none";
      state.sim.rightItem = "none";
      state.sim.leftCubes = 0;
      state.sim.rightCubes = 0;
      leftSelect.value = "none";
      rightSelect.value = "none";
      updateSimVisuals();
    });
  }

  function adjustCubes(side, delta) {
    const totalUsed = state.sim.leftCubes + state.sim.rightCubes;
    if (delta > 0 && totalUsed >= MAX_WEIGHT_UNITS) return;
    if (side === "left") {
      state.sim.leftCubes = Math.max(0, state.sim.leftCubes + delta);
    } else {
      state.sim.rightCubes = Math.max(0, state.sim.rightCubes + delta);
    }
    updateSimVisuals();
  }

  function rebuildPanGroup(group, itemId, cubeCount) {
    while (group.children.length > 0) {
      group.remove(group.children.pop());
    }
    const item = TEST_ITEMS.find((i) => i.id === itemId);
    let offsetZ = 0;
    if (item && item.grams > 0) {
      const [w, h, d] = item.size;
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        new THREE.MeshStandardMaterial({ color: item.color, roughness: 0.45 })
      );
      mesh.position.set(0, h / 2, -0.8);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      group.add(mesh);
      offsetZ = 2.8;
    }

    for (let i = 0; i < cubeCount; i++) {
      const gear = assembly.createPartMesh("GEAR20");
      const stack = Math.floor(i / 6);
      const idxInLayer = i % 6;
      const col = idxInLayer % 3;
      const row = Math.floor(idxInLayer / 3);
      gear.position.set((col - 1) * 2.15, 0.28 + stack * 0.56, offsetZ + (row - 0.5) * 2.15);
      group.add(gear);
    }
  }

  function updateSimVisuals() {
    leftCubeCount.textContent = state.sim.leftCubes;
    rightCubeCount.textContent = state.sim.rightCubes;

    const lItem = TEST_ITEMS.find((i) => i.id === state.sim.leftItem);
    const rItem = TEST_ITEMS.find((i) => i.id === state.sim.rightItem);
    const lTotal = (lItem ? lItem.grams : 0) + state.sim.leftCubes * UNIT_GRAMS;
    const rTotal = (rItem ? rItem.grams : 0) + state.sim.rightCubes * UNIT_GRAMS;

    leftTotalEl.textContent = `${lTotal} g`;
    rightTotalEl.textContent = `${rTotal} g`;

    const diff = lTotal - rTotal; // >0 左重 (逆時針正角)，<0 右重 (順時針負角)
    if (diff === 0) {
      readoutBox.classList.remove("tilted");
      readoutStatus.textContent = "兩邊一樣重（達成平衡！）";
      state.sim.targetAngle = 0;
    } else if (diff > 0) {
      readoutBox.classList.add("tilted");
      readoutStatus.textContent = `左邊較重（多 ${diff} g，左盤下降）`;
      state.sim.targetAngle = Math.min(0.24, 0.05 + (diff / 300) * 0.19);
    } else {
      readoutBox.classList.add("tilted");
      readoutStatus.textContent = `右邊較重（多 ${Math.abs(diff)} g，右盤下降）`;
      state.sim.targetAngle = -Math.min(0.24, 0.05 + (Math.abs(diff) / 300) * 0.19);
    }

    // 同步顯示模擬物品與預留區剩餘紅齒輪數
    rebuildPanGroup(leftPanLoadGroup, state.sim.leftItem, state.sim.leftCubes);
    rebuildPanGroup(rightPanLoadGroup, state.sim.rightItem, state.sim.rightCubes);

    const usedTotal = state.sim.leftCubes + state.sim.rightCubes;
    const reserveMeshes = assembly.reserveCubesGroup.children;
    reserveMeshes.forEach((m, idx) => {
      m.visible = state.mode === "simulate" ? idx < MAX_WEIGHT_UNITS - usedTotal : state.step >= 6;
    });
  }

  // ------------------------------------------------------------------------
  // 模式切換
  // ------------------------------------------------------------------------
  function setMode(mode) {
    state.mode = mode;
    tabBtns.forEach((b) => {
      const active = b.dataset.mode === mode;
      b.classList.toggle("active", active);
      b.setAttribute("aria-selected", active ? "true" : "false");
    });
    Object.keys(views).forEach((k) => {
      views[k].classList.toggle("active", k === mode);
    });

    if (mode === "simulate") {
      // 模擬模式自動關閉爆炸拆解並顯示完整結構
      state.explode = 0;
      explodeSlider.value = "0";
      explodeVal.textContent = "0%";
      explodeControl.style.display = "none";
      assembly.allParts.forEach((p) => { p.mesh.visible = true; });
      leftPanLoadGroup.visible = true;
      rightPanLoadGroup.visible = true;
      updateSimVisuals();
      moveCamera("front");
    } else {
      explodeControl.style.display = "flex";
      leftPanLoadGroup.visible = false;
      rightPanLoadGroup.visible = false;
      state.sim.targetAngle = 0;
      setStep(mode === "bom" ? 6 : state.step);
    }
    clearHighlights();
  }

  tabBtns.forEach((b) => b.addEventListener("click", () => setMode(b.dataset.mode)));

  // ------------------------------------------------------------------------
  // 點擊 3D 積木查閱官方品號（Raycaster）
  // ------------------------------------------------------------------------
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let pointerDownPos = { x: 0, y: 0 };

  renderer.domElement.addEventListener("pointerdown", (e) => {
    pointerDownPos = { x: e.clientX, y: e.clientY };
  });

  renderer.domElement.addEventListener("pointerup", (e) => {
    const dx = e.clientX - pointerDownPos.x;
    const dy = e.clientY - pointerDownPos.y;
    if (Math.hypot(dx, dy) > 6) return; // 拖曳旋轉不觸發點擊

    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(assembly.rootGroup.children, true);
    const hit = hits.find((h) => h.object.visible && h.object.userData.partMeta);

    if (hit) {
      const m = hit.object.userData.partMeta;
      inspSwatch.style.backgroundColor = m.swatch;
      inspCode.textContent = m.code;
      inspName.textContent = m.name;
      inspSpec.textContent = m.spec;
      inspStep.textContent = `步驟 ${m.step}`;
      inspRole.textContent = m.role;
      inspectorCard.hidden = false;
      highlightParts((p) => p === m);
    }
  });

  inspClose.addEventListener("click", () => {
    inspectorCard.hidden = true;
    clearHighlights();
  });

  // ------------------------------------------------------------------------
  // 日夜雙模切換
  // ------------------------------------------------------------------------
  btnTheme.addEventListener("click", () => {
    state.theme = state.theme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", state.theme);
    btnTheme.textContent = state.theme === "light" ? "🌙" : "☀️";
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) metaTheme.setAttribute("content", state.theme === "light" ? "#f8fafc" : "#0b1120");

    if (state.theme === "dark") {
      scene.background = new THREE.Color(0x0f172a);
      floorMat.color.setHex(0x111827);
      hemiLight.intensity = 0.72;
    } else {
      scene.background = new THREE.Color(0xe2e8f0);
      floorMat.color.setHex(0xf1f5f9);
      hemiLight.intensity = 0.85;
    }
  });

  // ------------------------------------------------------------------------
  // 視窗縮放適配
  // ------------------------------------------------------------------------
  window.addEventListener("resize", () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (w === 0 || h === 0) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });

  // ------------------------------------------------------------------------
  // 主動畫循環（爆炸插值 + 彈簧阻尼平衡物理 + 視角平滑移動）
  // ------------------------------------------------------------------------
  let lastTime = performance.now();

  function animate(now) {
    requestAnimationFrame(animate);
    const dt = Math.min(0.05, (now - lastTime) / 1000);
    lastTime = now;

    // 爆炸位移平滑插值
    assembly.allParts.forEach((p) => {
      const tx = p.basePos.x + p.explodeVec.x * state.explode;
      const ty = p.basePos.y + p.explodeVec.y * state.explode;
      const tz = p.basePos.z + p.explodeVec.z * state.explode;
      p.mesh.position.x += (tx - p.mesh.position.x) * 0.16;
      p.mesh.position.y += (ty - p.mesh.position.y) * 0.16;
      p.mesh.position.z += (tz - p.mesh.position.z) * 0.16;
    });

    // 等臂天平彈簧阻尼擺動物理
    const stiffness = 26;
    const damping = 5.2;
    const force = (state.sim.targetAngle - state.sim.angle) * stiffness;
    state.sim.angVel += force * dt;
    state.sim.angVel *= Math.exp(-damping * dt);
    state.sim.angle += state.sim.angVel * dt;
    assembly.pivotGroup.rotation.z = state.sim.angle;

    // 同步高亮框位置
    highlightBoxes.children.forEach((h) => h.update());

    // 視角預設平滑移動
    if (camAnim) {
      camAnim.t += dt * 2.4;
      const ease = 1 - Math.pow(1 - Math.min(1, camAnim.t), 3);
      camera.position.lerpVectors(camAnim.startPos, camAnim.endPos, ease);
      controls.target.lerpVectors(camAnim.startTarget, camAnim.endTarget, ease);
      if (camAnim.t >= 1) camAnim = null;
    }

    controls.update();
    renderer.render(scene, camera);
  }

  // 啟動初始化
  initStepDots();
  initSimSelects();
  renderBOM();
  setStep(6);
  leftPanLoadGroup.visible = false;
  rightPanLoadGroup.visible = false;
  requestAnimationFrame(animate);
})();
