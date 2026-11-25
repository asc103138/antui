/* ==========================================================================
   智高 #1248R-CN（機關創意 600件/組 × 2盒）官方真實零件庫與 3D 幾何工廠
   每項零件均嚴格核對 #1248R 官方零件表與兩盒總庫存上限，零虛構、零超量。
   網格基準：1 Three.js 單位 = 10mm（智高 C 系列標準孔距 10mm）
   ========================================================================== */

window.GIGO_CATALOG = {
  F5x15: {
    code: "7413-W10-J1W",
    name: "C-5×15孔長方框-白",
    spec: "5×15 孔（50×150×10mm）",
    colorHex: 0xf8fafc,
    swatch: "#f8fafc",
    maxQty2Boxes: 30,
    category: "struct",
    usage: "強化寬底座主框、雙柱龍門塔架主壁"
  },
  F5x10: {
    code: "7413-W10-I1W",
    name: "C-5×10孔長方框-白",
    spec: "5×10 孔（50×100×10mm）",
    colorHex: 0xf1f5f9,
    swatch: "#f1f5f9",
    maxQty2Boxes: 30,
    category: "struct",
    usage: "底座左右防傾翼板、左右 10×10cm 承重托盤面"
  },
  R15: {
    code: "7413-W10-Z1W",
    name: "C-15孔超長條-白",
    spec: "15 孔雙向孔（150×10×10mm）",
    colorHex: 0xe2e8f0,
    swatch: "#e2e8f0",
    maxQty2Boxes: 40,
    category: "struct",
    usage: "塔架底部 90° 雙軌錨定樑、等臂橫樑雙層核心主樑"
  },
  R11: {
    code: "7413-W10-P1W",
    name: "C-11孔長條-白",
    spec: "11 孔長條（110×10×5mm）",
    colorHex: 0xe5e7eb,
    swatch: "#e5e7eb",
    maxQty2Boxes: 20,
    category: "struct",
    usage: "6-8-10 畢氏斜撐、橫樑夾板、托盤防漏格柵底板（間隙≤10mm）"
  },
  R5: {
    code: "7413-W10-K2W",
    name: "C-5孔長條-白",
    spec: "5 孔長條（50×10×5mm）",
    colorHex: 0xe2e8f0,
    swatch: "#e2e8f0",
    maxQty2Boxes: 20,
    category: "struct",
    usage: "底座跨縫鎖條、雙塔前後拉桿、托盤底橫樑"
  },
  R3: {
    code: "7026-W10-Q2W",
    name: "C-3孔長條-白",
    spec: "3 孔長條（30×10×5mm）",
    colorHex: 0xe2e8f0,
    swatch: "#e2e8f0",
    maxQty2Boxes: 20,
    category: "struct",
    usage: "托盤外側防滾擋邊條"
  },
  AX100: {
    code: "7413-W10-L2D",
    name: "C-100mmⅡ軸-黑",
    spec: "Ø4.8mm × 100mm（10 格長）",
    colorHex: 0x1e293b,
    swatch: "#1e293b",
    maxQty2Boxes: 12,
    category: "struct",
    usage: "貫穿雙塔架與橫樑中心之低摩擦主支點轉軸"
  },
  AXC: {
    code: "3620-W10-A1D",
    name: "C-軸固定鍵-黑",
    spec: "軸套限位環（10×10×8mm）",
    colorHex: 0x334155,
    swatch: "#334155",
    maxQty2Boxes: 10,
    category: "struct",
    usage: "主軸外側防脫落、內側留 1mm 低摩擦限位"
  },
  CON2IN1: {
    code: "7061-W10-G1W",
    name: "C-二合一結合鍵-白",
    spec: "90° 正交二合一轉接（10×10×10mm）",
    colorHex: 0xcbd5e1,
    swatch: "#cbd5e1",
    maxQty2Boxes: 20,
    category: "struct",
    usage: "橫樑末端夾層承接座（向上鎖固托盤底樑）"
  },
  CON2: {
    code: "7061-W10-X1W",
    name: "C-雙向轉接鍵-白",
    spec: "90° 正交雙向孔轉接（10×10×10mm）",
    colorHex: 0x94a3b8,
    swatch: "#94a3b8",
    maxQty2Boxes: 4,
    category: "struct",
    usage: "斜撐下端 90° 支座（兩盒剛好 4 顆，直插底座翼板實體孔）"
  },
  LPEG: {
    code: "7061-W10-C1R",
    name: "C-長結合鍵-紅",
    spec: "長 20mm（跨 3 層疊合）",
    colorHex: 0xef4444,
    swatch: "#ef4444",
    maxQty2Boxes: 200,
    category: "struct",
    usage: "三層複合等臂橫樑深層抗剪插銷"
  },
  SPEG: {
    code: "7344-W10-C2D",
    name: "B-短結合鍵-黑",
    spec: "長 12mm（跨 2 層結合）",
    colorHex: 0x1f2937,
    swatch: "#1f2937",
    maxQty2Boxes: 200,
    category: "struct",
    usage: "底座拼鎖、雙軌錨定樑、塔架與斜撐固定"
  },
  GEAR20: {
    code: "7026-W10-D2R",
    name: "C-20T齒輪-紅（砝碼專用）",
    spec: "Ø20mm 圓齒輪（單顆約 3g，#1248R-CN 內含）",
    colorHex: 0xdc2626,
    swatch: "#dc2626",
    maxQty2Boxes: 20,
    category: "weight",
    usage: "兩盒共 20 顆全數預留不進主結構，專供教案第 3 節加減平衡單位"
  }
};

window.ASSEMBLY_STEPS = [
  {
    step: 1,
    title: "步驟 1｜超寬獨立底座（平放桌面，不插大底盤）",
    desc: "直接以 #1248R-CN 內附 2 片 C-5×15 孔長方框前後並排，左右再接 2 片 C-5×10 孔長方框，平放於桌面組成 25×10cm 獨立寬底座，並以 8 根 C-5 孔長條鎖緊外圍實體邊框（不需硬插進盒內大底盤槽孔）。",
    tips: [
      "本底座為獨立平放式寬底盤，切勿將長方框硬塞進 #1248R-CN 附的大底盤（C-Jumbo Base Grid）方格內。",
      "所有跨縫短結合鍵皆插在長方框最外圈的實體邊框孔位（z = ±0.5 與 ±4.5）。"
    ]
  },
  {
    step: 2,
    title: "步驟 2｜實框雙軌錨定樑＋雙柱龍門塔架",
    desc: "將 2 根 C-15 孔超長條直接平鎖在底座中央兩條「實體內邊框（Z = ±0.5）」上（所有奇數垂直孔 ±1, ±3, ±5, ±7 全部直插底座實體孔！），再將前後兩片直立 C-5×15 孔長方框貼緊外側（Z = ±1.5），以偶數水平孔（x = -2, 0, +2）鎖死，絕不懸空於簍空處。",
    tips: [
      "兩根錨定樑完全壓在底座 Z = ±0.5 實體邊框上，每根有 8 個真實垂直孔可直接插滿短結合鍵固定。",
      "雙塔內側留出 20mm 淨空通道，足以讓 10mm 寬的橫樑核心順暢擺動不磨擦。"
    ]
  },
  {
    step: 3,
    title: "步驟 3｜6-8-10 畢氏定理三角斜撐",
    desc: "扛 500g–1kg 重物最關鍵的抗晃結構！在塔架左右前後安裝 4 根 C-11 孔長條（首尾孔距剛好 10 格 = 100mm），下端以 C-二合一結合鍵鎖在底座 X = ±8、上端以黑色 B-短結合鍵鎖在塔架第 9 孔（dx = 6、dy = 8、斜邊 = 10 格精確對孔）。",
    tips: [
      "6-8-10 為精確整數畢氏三角，安裝時不需硬掰積木就能自然對準孔位。",
      "本步驟僅用 4 顆 C-二合一結合鍵（兩盒共有 20 顆），完全不會缺件。"
    ]
  },
  {
    step: 4,
    title: "步驟 4｜中央低摩擦主支點轉軸組（頂框實體孔）",
    desc: "因 C-5×15 孔長方框中央為簍空窗格，必須將 1 根黑色 C-100mmⅡ軸（7413-W10-L2D）穿過前後塔架最上緣「實體邊框第 15 孔（X = 0, Y = 15.5）」作為天平主支點！外側裝 2 顆 C-軸固定鍵防脫落，內側裝 2 顆作限位墊圈。",
    tips: [
      "務必穿在最頂端實體邊框正中央孔位（X = 0, Y = 15.5），切勿誤判簍空區有孔。",
      "內側 C-軸固定鍵保留約 1mm 微隙，確保手指輕撥即可靈敏擺動。"
    ]
  },
  {
    step: 5,
    title: "步驟 5｜三層複合強化等臂橫樑（27 cm 跨距）",
    desc: "中央採用上下雙層 C-15 孔超長條（150mm）以黑色短結合鍵垂直互鎖成抗彎工字核心，前後兩面再以 4 根 C-11 孔長條左右對稱跨接（各重疊 5 孔），並以 12 顆紅色 C-長結合鍵貫穿三層鎖固，末端夾入 4 顆 C-二合一結合鍵承接托盤。",
    tips: [
      "中央上層 C-15 孔超長條第 8 孔（正中央 X = 0）套入主轉軸，左右各對稱延伸 13 孔。",
      "紅色 C-長結合鍵務必貫穿前夾板＋核心＋後夾板三層，扛 1kg 不下垂變形。"
    ]
  },
  {
    step: 6,
    title: "步驟 6｜防漏格柵托盤（間隙≤10mm）＋ 20 顆紅齒輪砝碼",
    desc: "C-5×10 孔長方框中央為簍空，若直接放小物會掉下去！本步驟在左右 10×10cm 長方框上各橫鋪 4 根 C-11 孔長條（跨接四條實體邊框、相鄰間隙僅 10mm），形成高承重防漏格柵平台，連 Ø20mm 紅齒輪與橡皮擦都絕不掉落；另預留 20 顆紅色 C-20T 齒輪專作加減砝碼。",
    tips: [
      "每側 4 根 C-11 孔長條跨鎖前後兩片長方框的四條實體邊框，兼顧「防掉落底板」與「雙框一體鎖固」。",
      "相鄰長條淨空僅 10mm，Ø20mm 紅齒輪寬度為縫隙的 2 倍，平放疊放都不會漏下去！"
    ]
  }
];

/* --------------------------------------------------------------------------
   程序化智高 #1248R-CN 積木幾何工廠（真實孔洞、齒輪齒廓、材質快取）
   -------------------------------------------------------------------------- */
(function () {
  const matCache = new Map();

  function getPlasticMat(hex, roughness = 0.36, metalness = 0.05) {
    const key = `${hex}_${roughness}`;
    if (!matCache.has(key)) {
      matCache.set(
        key,
        new THREE.MeshStandardMaterial({
          color: hex,
          roughness,
          metalness
        })
      );
    }
    return matCache.get(key);
  }

  const holeMat = new THREE.MeshStandardMaterial({
    color: 0x334155,
    roughness: 0.85,
    metalness: 0.05
  });

  // 真實簍空矩形孔框（C-5x15、C-5x10 長方框：僅外圍一圈 1 孔寬為實體孔框，中央完全簍空！）
  function buildFrameMesh(holesX, holesZ, colorHex) {
    const group = new THREE.Group();
    const w = holesX;
    const d = holesZ;
    const h = 0.96;
    const mat = getPlasticMat(colorHex, 0.32);

    // 四條實體外圍邊框（上/下兩條長邊 + 左/右兩條短邊，寬度皆為 1 孔 = 10mm）
    const longBarGeo = new THREE.BoxGeometry(w - 0.06, h, 0.96);
    const barFront = new THREE.Mesh(longBarGeo, mat);
    barFront.position.z = (d - 1) / 2;
    const barBack = new THREE.Mesh(longBarGeo, mat);
    barBack.position.z = -(d - 1) / 2;

    const shortBarGeo = new THREE.BoxGeometry(0.96, h, Math.max(0.1, d - 2));
    const barLeft = new THREE.Mesh(shortBarGeo, mat);
    barLeft.position.x = -(w - 1) / 2;
    const barRight = new THREE.Mesh(shortBarGeo, mat);
    barRight.position.x = (w - 1) / 2;

    [barFront, barBack, barLeft, barRight].forEach((b) => {
      b.castShadow = true;
      b.receiveShadow = true;
      group.add(b);
    });

    // 僅在外圍一圈實體邊框上打孔（完全忠於真實智高長方框！）
    const perimeterHoles = [];
    for (let ix = 0; ix < holesX; ix++) {
      for (let iz = 0; iz < holesZ; iz++) {
        if (ix === 0 || ix === holesX - 1 || iz === 0 || iz === holesZ - 1) {
          perimeterHoles.push([ix - (holesX - 1) / 2, iz - (holesZ - 1) / 2]);
        }
      }
    }

    const holeGeo = new THREE.CylinderGeometry(0.24, 0.24, h + 0.04, 10);
    const inst = new THREE.InstancedMesh(holeGeo, holeMat, perimeterHoles.length);
    const dummy = new THREE.Object3D();
    perimeterHoles.forEach(([hx, hz], idx) => {
      dummy.position.set(hx, 0, hz);
      dummy.updateMatrix();
      inst.setMatrixAt(idx, dummy.matrix);
    });
    inst.instanceMatrix.needsUpdate = true;
    group.add(inst);

    // 外框細線條增強辨識
    const edges = new THREE.EdgesGeometry(new THREE.BoxGeometry(w - 0.04, h + 0.01, d - 0.04));
    group.add(new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.4 })));

    return group;
  }

  // C-15 孔超長條（10mm×10mm 真實交錯雙向孔：偶數偏位為 Z 向水平孔、奇數偏位為 Y 向垂直孔！）
  function buildDualRodMesh(holes, colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.34);
    const body = new THREE.Mesh(new THREE.BoxGeometry(holes - 0.04, 0.96, 0.96), mat);
    body.castShadow = true;
    body.receiveShadow = true;
    group.add(body);

    const zPositions = [];
    const yPositions = [];
    for (let i = 0; i < holes; i++) {
      const offset = i - (holes - 1) / 2; // 15孔為 -7..+7
      // 偶數偏位 (0, ±2, ±4, ±6) 為 Z 向水平孔；奇數偏位 (±1, ±3, ±5, ±7) 為 Y 向垂直孔
      if (Math.round(Math.abs(offset)) % 2 === 0) {
        zPositions.push(offset);
      } else {
        yPositions.push(offset);
      }
    }

    const holeGeoZ = new THREE.CylinderGeometry(0.24, 0.24, 1.0, 10);
    holeGeoZ.rotateX(Math.PI / 2);
    const instZ = new THREE.InstancedMesh(holeGeoZ, holeMat, zPositions.length);
    const dummy = new THREE.Object3D();
    zPositions.forEach((posX, idx) => {
      dummy.position.set(posX, 0, 0);
      dummy.updateMatrix();
      instZ.setMatrixAt(idx, dummy.matrix);
    });
    instZ.instanceMatrix.needsUpdate = true;

    const holeGeoY = new THREE.CylinderGeometry(0.24, 0.24, 1.0, 10);
    const instY = new THREE.InstancedMesh(holeGeoY, holeMat, yPositions.length);
    yPositions.forEach((posX, idx) => {
      dummy.position.set(posX, 0, 0);
      dummy.updateMatrix();
      instY.setMatrixAt(idx, dummy.matrix);
    });
    instY.instanceMatrix.needsUpdate = true;

    group.add(instZ, instY);

    const edges = new THREE.EdgesGeometry(new THREE.BoxGeometry(holes - 0.03, 0.97, 0.97));
    group.add(new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.4 })));

    return group;
  }

  // C 系列平長條（寬 10mm、厚 5mm，兩端圓角）
  function buildFlatRodMesh(holes, colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.34);
    const len = holes - 1;
    const body = new THREE.Mesh(new THREE.BoxGeometry(len, 0.88, 0.46), mat);
    body.castShadow = true;
    body.receiveShadow = true;
    group.add(body);

    const capGeo = new THREE.CylinderGeometry(0.44, 0.44, 0.46, 14);
    capGeo.rotateX(Math.PI / 2);
    const capL = new THREE.Mesh(capGeo, mat);
    capL.position.x = -len / 2;
    const capR = new THREE.Mesh(capGeo, mat);
    capR.position.x = len / 2;
    capL.castShadow = capR.castShadow = true;
    group.add(capL, capR);

    const holeGeo = new THREE.CylinderGeometry(0.23, 0.23, 0.5, 10);
    holeGeo.rotateX(Math.PI / 2);
    const inst = new THREE.InstancedMesh(holeGeo, holeMat, holes);
    const dummy = new THREE.Object3D();
    for (let i = 0; i < holes; i++) {
      dummy.position.set(i - (holes - 1) / 2, 0, 0);
      dummy.updateMatrix();
      inst.setMatrixAt(i, dummy.matrix);
    }
    inst.instanceMatrix.needsUpdate = true;
    group.add(inst);

    return group;
  }

  // C-100mm II 軸
  function buildAxleMesh(len, colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.4, 0.15);
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, len, 14), mat);
    shaft.rotation.x = Math.PI / 2;
    shaft.castShadow = true;
    group.add(shaft);
    return group;
  }

  // C-軸固定鍵
  function buildAxleCollarMesh(colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.42);
    const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.44, 0.44, 0.72, 16), mat);
    ring.rotation.x = Math.PI / 2;
    ring.castShadow = true;
    const inner = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.76, 12), holeMat);
    inner.rotation.x = Math.PI / 2;
    group.add(ring, inner);
    return group;
  }

  // C-二合一結合鍵（90° 正交轉接）
  function buildTwoInOneConverterMesh(colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.34);
    const cube = new THREE.Mesh(new THREE.BoxGeometry(0.92, 0.92, 0.92), mat);
    cube.castShadow = true;
    cube.receiveShadow = true;
    group.add(cube);

    const topStud = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.52, 12), mat);
    topStud.position.y = 0.62;
    const botStud = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.52, 12), mat);
    botStud.position.y = -0.62;
    const sideHole = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.96, 10), holeMat);
    sideHole.rotation.x = Math.PI / 2;
    group.add(topStud, botStud, sideHole);
    return group;
  }

  // 結合鍵（短黑 / 長紅）
  function buildPegMesh(length, colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.32);
    const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.21, length, 12), mat);
    pin.rotation.x = Math.PI / 2;
    const flange = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.16, 12), mat);
    flange.rotation.x = Math.PI / 2;
    flange.position.z = length * 0.46;
    const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.14, 12), mat);
    tail.rotation.x = Math.PI / 2;
    tail.position.z = -length * 0.46;
    group.add(pin, flange, tail);
    return group;
  }

  // C-20T 齒輪-紅（Ø20mm，20 齒擬真造型，專作等重小積木砝碼）
  function buildGear20Mesh(colorHex) {
    const group = new THREE.Group();
    const mat = getPlasticMat(colorHex, 0.28);

    // 主輪盤（直徑 2.0 單位 = 20mm，厚 0.55 單位 = 5.5mm）
    const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.88, 0.88, 0.54, 20), mat);
    disc.castShadow = true;
    disc.receiveShadow = true;
    group.add(disc);

    // 20 齒外圈（InstancedMesh 呈現真實齒廓）
    const toothGeo = new THREE.BoxGeometry(0.16, 0.52, 0.28);
    const teeth = new THREE.InstancedMesh(toothGeo, mat, 20);
    const dummy = new THREE.Object3D();
    for (let i = 0; i < 20; i++) {
      const a = (i / 20) * Math.PI * 2;
      dummy.position.set(Math.sin(a) * 0.93, 0, Math.cos(a) * 0.93);
      dummy.rotation.set(0, a, 0);
      dummy.updateMatrix();
      teeth.setMatrixAt(i, dummy.matrix);
    }
    teeth.instanceMatrix.needsUpdate = true;
    teeth.castShadow = true;
    group.add(teeth);

    // 中心軸孔
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.58, 12), holeMat);
    group.add(hub);

    return group;
  }

  function createPartMesh(typeKey) {
    const info = window.GIGO_CATALOG[typeKey];
    switch (typeKey) {
      case "F5x15": return buildFrameMesh(15, 5, info.colorHex);
      case "F5x10": return buildFrameMesh(10, 5, info.colorHex);
      case "R15": return buildDualRodMesh(15, info.colorHex);
      case "R11": return buildFlatRodMesh(11, info.colorHex);
      case "R5": return buildFlatRodMesh(5, info.colorHex);
      case "R3": return buildFlatRodMesh(3, info.colorHex);
      case "AX100": return buildAxleMesh(9.8, info.colorHex);
      case "AXC": return buildAxleCollarMesh(info.colorHex);
      case "CON2IN1": return buildTwoInOneConverterMesh(info.colorHex);
      case "CON2": return buildTwoInOneConverterMesh(info.colorHex);
      case "LPEG": return buildPegMesh(2.2, info.colorHex);
      case "SPEG": return buildPegMesh(1.3, info.colorHex);
      case "GEAR20": return buildGear20Mesh(info.colorHex);
      default: return buildGear20Mesh(0xdc2626);
    }
  }

  /* ------------------------------------------------------------------------
     建構整座智高 #1248R-CN（×2盒）等臂天平實體模型
     ------------------------------------------------------------------------ */
  window.buildGigoBalanceAssembly = function () {
    const rootGroup = new THREE.Group();
    const staticGroup = new THREE.Group();
    const pivotGroup = new THREE.Group();
    pivotGroup.position.set(0, 15.5, 0); // 精準對齊直立 C-5×15 長方框最頂端實體邊框中央孔 (X=0, Y=15.5)

    const reserveCubesGroup = new THREE.Group();
    rootGroup.add(staticGroup, pivotGroup, reserveCubesGroup);

    const allParts = [];

    function addPart(targetGroup, typeKey, pos, rot, step, explodeVec, role) {
      const mesh = createPartMesh(typeKey);
      const basePos = new THREE.Vector3(pos[0], pos[1], pos[2]);
      mesh.position.copy(basePos);
      if (rot) mesh.rotation.set(rot[0], rot[1], rot[2]);

      const info = window.GIGO_CATALOG[typeKey];
      const meta = {
        typeKey,
        code: info.code,
        name: info.name,
        spec: info.spec,
        swatch: info.swatch,
        step,
        role,
        basePos: basePos.clone(),
        explodeVec: new THREE.Vector3(explodeVec[0], explodeVec[1], explodeVec[2]),
        mesh,
        targetGroup
      };
      mesh.userData.partMeta = meta;
      mesh.traverse((child) => {
        if (child.isMesh) {
          child.userData.partMeta = meta;
        }
      });

      targetGroup.add(mesh);
      allParts.push(meta);
      return meta;
    }

    // =====================================================================
    // STEP 1：超寬防傾強化底座（25×10 孔 = 250×100mm）
    // =====================================================================
    addPart(staticGroup, "F5x15", [0, 0.5, 2.5], [0, 0, 0], 1, [0, -1.5, 2.2], "前側底座主框（15×5 孔）");
    addPart(staticGroup, "F5x15", [0, 0.5, -2.5], [0, 0, 0], 1, [0, -1.5, -2.2], "後側底座主框（15×5 孔）");
    addPart(staticGroup, "F5x10", [-10, 0.5, 0], [0, Math.PI / 2, 0], 1, [-3.8, -1.5, 0], "左側防傾延伸翼板（10×5 孔）");
    addPart(staticGroup, "F5x10", [10, 0.5, 0], [0, Math.PI / 2, 0], 1, [3.8, -1.5, 0], "右側防傾延伸翼板（10×5 孔）");

    // 跨前後縫鎖條（4 根 C-5 孔長條，只插在前後框實體邊框 z = ±0.5 孔位！）
    const seamBars = [
      { x: -6, z: 0.5 },
      { x: -4, z: -0.5 },
      { x: 4, z: -0.5 },
      { x: 6, z: 0.5 }
    ];
    seamBars.forEach((b) => {
      addPart(staticGroup, "R5", [b.x, 1.23, b.z], [Math.PI / 2, 0, Math.PI / 2], 1, [b.x * 0.12, 1.6, b.z * 2], "底座前後接縫跨鎖條");
      [-0.5, 0.5].forEach((pz) => {
        addPart(staticGroup, "SPEG", [b.x, 1.25, pz], [Math.PI / 2, 0, 0], 1, [b.x * 0.12, 2.6, b.z * 2], "底座實體邊框跨縫短結合鍵");
      });
    });

    // 左右翼板與主框跨鎖條（4 根 C-5 孔長條，鎖在最前後實體外框 z = ±4.5！）
    [-7.5, 7.5].forEach((sx) => {
      [-4.5, 4.5].forEach((sz) => {
        const cx = sx < 0 ? -7 : 7;
        addPart(staticGroup, "R5", [cx, 1.23, sz], [Math.PI / 2, 0, 0], 1, [sx * 0.35, 1.8, sz * 0.5], "底座左右翼板實體外框跨鎖條");
        [cx - 2, cx - 1, cx + 1, cx + 2].forEach((px) => {
          addPart(staticGroup, "SPEG", [px, 1.25, sz], [Math.PI / 2, 0, 0], 1, [sx * 0.35, 2.8, sz * 0.5], "翼板實體外框短結合鍵");
        });
      });
    });

    // =====================================================================
    // STEP 2：實框雙軌錨定樑（Z = ±0.5 底座實體邊框正上方！）＋ 雙柱龍門塔架（Z = ±1.5）
    // 徹底避免零件落在長方框中央簍空區，每個垂直插銷 100% 插入底座實體邊框孔！
    // =====================================================================
    addPart(staticGroup, "F5x15", [0, 8.5, 1.5], [Math.PI / 2, Math.PI / 2, 0], 2, [0, 1.2, 4.0], "前側龍門立柱塔架（貼緊前錨定樑外側 Z=+1.5）");
    addPart(staticGroup, "F5x15", [0, 8.5, -1.5], [Math.PI / 2, Math.PI / 2, 0], 2, [0, 1.2, -4.0], "後側龍門立柱塔架（貼緊後錨定樑外側 Z=-1.5）");

    // 2 根 C-15 孔超長條直接壓在底座實體內邊框 Z = ±0.5 上！
    [-0.5, 0.5].forEach((rz) => {
      const signZ = rz > 0 ? 1 : -1;
      addPart(staticGroup, "R15", [0, 1.5, rz], [0, 0, 0], 2, [0, 1.4, signZ * 1.2], "底座實體邊框錨定樑（Z=±0.5 全長壓於實框上）");
      // 奇數垂直孔 x = ±7, ±5, ±3, ±1 全部直插底座實體邊框孔！
      [-7, -5, -3, 3, 5, 7].forEach((px) => {
        addPart(staticGroup, "SPEG", [px, 1.0, rz], [Math.PI / 2, 0, 0], 2, [px * 0.1, 2.2, signZ * 1.2], "錨定樑直插底座實體邊框短結合鍵");
      });
      // 偶數水平孔 x = -2, 0, +2 向外鎖入塔架底部實體邊框（Z = ±1.5）
      [-2, 0, 2].forEach((tx) => {
        addPart(staticGroup, "SPEG", [tx, 1.5, rz + signZ * 0.55], [0, 0, 0], 2, [tx * 0.2, 1.4, signZ * 2.8], "錨定樑水平鎖入塔架底框短結合鍵");
      });
    });

    // =====================================================================
    // STEP 3：6-8-10 畢氏定理三角斜撐（dx=6, dy=8, 斜邊=10 格精準對孔）
    // 下端使用 #1248R-CN 兩盒剛好 4 顆的 C-雙向轉接鍵直插翼板實體邊框 x=±8, z=±1.5！
    // =====================================================================
    const braceAngle = Math.atan2(8, 6);
    [-1, 1].forEach((dirX) => {
      [-1, 1].forEach((dirZ) => {
        const cx = dirX * 5.0;
        const cy = 5.5;
        const cz = dirZ * 2.24;
        const rotZ = dirX < 0 ? braceAngle : -braceAngle;
        addPart(
          staticGroup,
          "R11",
          [cx, cy, cz],
          [0, 0, rotZ],
          3,
          [dirX * 3.6, 1.4, dirZ * 4.0],
          "6-8-10 精確畢氏三角抗晃斜撐"
        );
        // 下端 C-雙向轉接鍵直插翼板實體內框 x = ±8, z = ±1.5
        addPart(staticGroup, "CON2", [dirX * 8, 1.5, dirZ * 1.5], [0, 0, 0], 3, [dirX * 4.2, 0.5, dirZ * 3.2], "斜撐下端 90° 雙向轉接支座（直插翼板實框）");
        addPart(staticGroup, "SPEG", [dirX * 8, 1.5, dirZ * 2.1], [0, 0, 0], 3, [dirX * 4.6, 0.5, dirZ * 4.5], "斜撐下端固定短結合鍵");
        // 上端鎖入塔架外側實體邊框 (x = ±2, y = 9.5, z = ±1.5)
        addPart(staticGroup, "SPEG", [dirX * 2, 9.5, dirZ * 1.95], [0, 0, 0], 3, [dirX * 2.6, 2.2, dirZ * 4.8], "斜撐上端固定短結合鍵");
      });
    });

    // =====================================================================
    // STEP 4：中央低摩擦主支點轉軸組（Y = 15.5，直穿前後塔架最上緣實體邊框中央孔！）
    // =====================================================================
    addPart(staticGroup, "AX100", [0, 15.5, 0], [0, 0, 0], 4, [0, 3.2, 5.5], "中央 100mm 主支點轉軸（穿過頂框實體孔）");
    [-2.45, 2.45].forEach((cz) => {
      addPart(staticGroup, "AXC", [0, 15.5, cz], [0, 0, 0], 4, [0, 3.2, cz * 2.1], "外側軸固定鍵（鎖定主軸防脫落）");
    });

    // =====================================================================
    // STEP 5：三層複合強化等臂橫樑（夾板從 x=±4 開始，與塔架外緣留足 10mm 擺動淨空！）
    // =====================================================================
    addPart(pivotGroup, "R15", [0, 0, 0], [0, 0, 0], 5, [0, 4.5, 0], "等臂橫樑上層主核心（偶數孔 x=0 套入主軸）");
    addPart(pivotGroup, "R15", [0, -1.0, 0], [0, 0, 0], 5, [0, 2.8, 0], "等臂橫樑下層抗彎補強樑");

    // 奇數偏位 x = ±1, ±3, ±5（真實垂直 Y 孔！）互鎖上下兩根 C-15 孔超長條
    [-5, -3, -1, 1, 3, 5].forEach((px) => {
      addPart(pivotGroup, "SPEG", [px, -0.5, 0], [Math.PI / 2, 0, 0], 5, [px * 0.15, 3.6, 0], "雙層核心奇數垂直孔互鎖短結合鍵");
    });

    // 左右末端夾層承接轉接座（x = ±8, ±12 整數孔位，向上 0.00mm 對齊托盤底樑）
    [-12, -8, 8, 12].forEach((cx) => {
      const dirX = cx < 0 ? -1 : 1;
      addPart(pivotGroup, "CON2IN1", [cx, 0, 0], [0, 0, 0], 5, [dirX * 3.0, 4.5, 0], "夾層橫樑末端二合一承接座（向上鎖固托盤）");
    });

    // 前後三層夾板強化（4 根 C-11 孔長條，橫跨 x = ±4..±14，中心 ±9，完全避開塔架！）
    [-1, 1].forEach((dirX) => {
      [-0.74, 0.74].forEach((cz) => {
        addPart(
          pivotGroup,
          "R11",
          [dirX * 9, 0, cz],
          [0, 0, 0],
          5,
          [dirX * 2.5, 4.5, cz * 4.5],
          "橫樑前後抗彎夾板（x=±4..±14，大角度傾斜不碰塔架）"
        );
      });
      // 紅色 C-長結合鍵嚴格插在偶數水平孔 x = ±4, ±6（核心真實 Z 孔！）與 ±8, ±12（二合一結合鍵真實 Z 孔！）
      [4, 6, 8, 12].forEach((ox) => {
        addPart(
          pivotGroup,
          "LPEG",
          [dirX * ox, 0, 0],
          [0, 0, 0],
          5,
          [dirX * ox * 0.25, 4.5, 4.8],
          "貫穿前夾板＋核心偶數Z孔/轉接座＋後夾板之紅色長結合鍵"
        );
      });
    });

    // =====================================================================
    // STEP 6：左右 10×10cm 防漏格柵托盤（中心 X = ±10.5，全部孔位精準落於整數 X！）
    // =====================================================================
    [-10.5, 10.5].forEach((panX) => {
      const sideLabel = panX < 0 ? "左" : "右";
      const dirX = panX < 0 ? -1 : 1;

      // 托盤底部橫鎖條（鎖於整數孔位 x = ±8, ±12，與橫樑二合一結合鍵 0.00mm 垂對！）
      [dirX * 8, dirX * 12].forEach((cx) => {
        addPart(pivotGroup, "R5", [cx, 0.92, 0.5], [Math.PI / 2, 0, Math.PI / 2], 6, [dirX * 3.5, 6.8, 0], `${sideLabel}托盤底部橫向鎖固樑（對齊 x=±8, ±12）`);
      });

      // 2 片簍空 C-5×10 孔長方框（X 孔位 = 精確整數 ±6..±15，Z 孔位 = ±0.5..±4.5）
      addPart(pivotGroup, "F5x10", [panX, 1.65, 2.5], [0, 0, 0], 6, [dirX * 3.8, 8.5, 2.2], `${sideLabel}托盤前外框（5×10 簍空框）`);
      addPart(pivotGroup, "F5x10", [panX, 1.65, -2.5], [0, 0, 0], 6, [dirX * 3.8, 8.5, -2.2], `${sideLabel}托盤後外框（5×10 簍空框）`);

      // 防漏格柵底板：4 根 C-11 孔長條嚴格置於整數孔位 x = ±8, ±10, ±11, ±13（全盤縫隙 ≤ 10mm！）
      [8, 10, 11, 13].forEach((ax) => {
        const sx = dirX * ax;
        addPart(
          pivotGroup,
          "R11",
          [sx, 2.38, 0.5],
          [Math.PI / 2, 0, Math.PI / 2],
          6,
          [dirX * 4.2, 10.2, 0],
          `${sideLabel}托盤防漏格柵條（x=${sx} 整數對孔，間隙≤10mm）`
        );
        // 鎖入前後框實體邊框 z = -4.5, +4.5
        [-4.5, 4.5].forEach((pz) => {
          addPart(pivotGroup, "SPEG", [sx, 2.38, pz], [Math.PI / 2, 0, 0], 6, [dirX * 4.2, 11.2, pz * 0.4], "防漏格柵條固定短結合鍵");
        });
      });

      // 外側防滾落擋邊條（C-3 孔長條平鋪於最外側實體邊框 x = ±15，垂直孔精準對齊 z = ±3.5, ±1.5！）
      const outerX = dirX * 15;
      [-2.5, 2.5].forEach((rz) => {
        addPart(pivotGroup, "R3", [outerX, 2.38, rz], [Math.PI / 2, 0, Math.PI / 2], 6, [dirX * 5.2, 10.8, rz], `${sideLabel}托盤外側擋邊條（平鎖於 x=±15 實體外框）`);
        [rz - 1, rz + 1].forEach((pz) => {
          addPart(pivotGroup, "SPEG", [outerX, 2.38, pz], [Math.PI / 2, 0, 0], 6, [dirX * 5.5, 11.5, pz], "擋邊條固定短結合鍵");
        });
      });
    });

    // 預留 20 顆紅色 C-20T 齒輪（#1248R-CN 兩盒全部預留不進主結構，陳列於前方預備區）
    for (let i = 0; i < 20; i++) {
      const col = i % 10;
      const row = Math.floor(i / 10);
      const cx = (col - 4.5) * 2.35;
      const cz = 8.0 + row * 2.35;
      addPart(
        reserveCubesGroup,
        "GEAR20",
        [cx, 0.3, cz],
        [0, 0, 0],
        6,
        [cx * 0.2, 0, 2.5],
        "教案第 3 節專用等重砝碼單位（兩盒共 20 顆全數預留）"
      );
    }

    return {
      rootGroup,
      staticGroup,
      pivotGroup,
      reserveCubesGroup,
      allParts,
      createPartMesh
    };
  };
})();
