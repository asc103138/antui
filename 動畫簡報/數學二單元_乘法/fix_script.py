from pathlib import Path

script_content = """  <!-- ==========================================
       現代簡報與三大關鍵動畫核心控制器
       ========================================== -->
  <script>
    const TOTAL_SLIDES = 14;
    let currentSlide = 1;

    // 初始化進度指示點
    const dotsContainer = document.getElementById('progress-dots');
    for (let i = 1; i <= TOTAL_SLIDES; i++) {
      const dot = document.createElement('div');
      dot.className = `dot ${i === 1 ? 'active' : ''}`;
      dot.onclick = () => goToSlide(i);
      dotsContainer.appendChild(dot);
    }

    function updateDeckUI() {
      // 切換頁面
      document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
      const activeSlide = document.querySelector(`.slide[data-slide="${currentSlide}"]`);
      if (activeSlide) activeSlide.classList.add('active');

      // 更新指示點
      document.querySelectorAll('.dot').forEach((d, idx) => {
        d.classList.toggle('active', idx + 1 === currentSlide);
      });

      // 更新頁碼
      document.getElementById('slide-counter').textContent = 
        `${String(currentSlide).padStart(2, '0')} / ${String(TOTAL_SLIDES).padStart(2, '0')}`;

      // 換頁時若切入關鍵頁，自動重置或觸發自訂狀態
      if (currentSlide === 5 && !animStates[1].hasInit) {
        setAnimProgress(1, 0);
        animStates[1].hasInit = true;
      }
      if (currentSlide === 6 && !animStates[2].hasInit) {
        setAnimProgress(2, 0);
        animStates[2].hasInit = true;
      }
      if (currentSlide === 8 && !animStates[3].hasInit) {
        setAnimProgress(3, 0);
        animStates[3].hasInit = true;
      }
    }

    function changeSlide(direction) {
      currentSlide = Math.max(1, Math.min(TOTAL_SLIDES, currentSlide + direction));
      updateDeckUI();
    }

    function goToSlide(slideNum) {
      currentSlide = Math.max(1, Math.min(TOTAL_SLIDES, slideNum));
      updateDeckUI();
    }

    // 鍵盤導航
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        changeSlide(1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        changeSlide(-1);
      }
    });

    // 小偵探診斷卡片點擊切換
    function toggleMyth(id) {
      const fb = document.getElementById(`myth-fb-${id}`);
      if (fb) {
        fb.classList.toggle('show');
      }
    }

    /* ==========================================================================
       三大關鍵頁動畫引擎 (Animation Players 1, 2, 3)
       支援：播放、暫停、滑桿拖拉 (0~100%)、分步前進後退、時間碼顯示
       ========================================================================== */
    const animStates = {
      1: { isPlaying: false, progress: 0, timer: null, hasInit: false, duration: 4.0 },
      2: { isPlaying: false, progress: 0, timer: null, hasInit: false, duration: 6.0 },
      3: { isPlaying: false, progress: 0, timer: null, hasInit: false, duration: 3.0 }
    };

    function togglePlay(id) {
      const state = animStates[id];
      if (state.isPlaying) {
        pauseAnim(id);
      } else {
        playAnim(id);
      }
    }

    function playAnim(id) {
      const state = animStates[id];
      state.isPlaying = true;
      const btn = document.getElementById(`btn-play-${id}`);
      if (btn) btn.textContent = '⏸';

      if (state.progress >= 100) {
        state.progress = 0;
      }

      const stepTimeMs = 40;
      const totalSteps = (state.duration * 1000) / stepTimeMs;
      const deltaPercent = 100 / totalSteps;

      clearInterval(state.timer);
      state.timer = setInterval(() => {
        state.progress += deltaPercent;
        if (state.progress >= 100) {
          state.progress = 100;
          pauseAnim(id);
        }
        applyAnimProgress(id, state.progress);
      }, stepTimeMs);
    }

    function pauseAnim(id) {
      const state = animStates[id];
      state.isPlaying = false;
      clearInterval(state.timer);
      const btn = document.getElementById(`btn-play-${id}`);
      if (btn) btn.textContent = '▶';
    }

    function onSliderInput(id, val) {
      pauseAnim(id);
      animStates[id].progress = parseFloat(val);
      applyAnimProgress(id, animStates[id].progress);
    }

    function stepAnim(id, dir) {
      pauseAnim(id);
      let p = animStates[id].progress + dir * 25;
      p = Math.max(0, Math.min(100, p));
      animStates[id].progress = p;
      applyAnimProgress(id, p);
    }

    function setAnimProgress(id, percent) {
      animStates[id].progress = percent;
      applyAnimProgress(id, percent);
    }

    function applyAnimProgress(id, p) {
      // 更新滑桿值
      const slider = document.getElementById(`slider-${id}`);
      if (slider) slider.value = p;

      // 更新時間/狀態碼
      const status = document.getElementById(`status-${id}`);
      const sec = (animStates[id].duration * (p / 100)).toFixed(1);
      const totalSec = animStates[id].duration.toFixed(1);

      // 依頁面特定呈現
      if (id === 1) {
        if (status) status.textContent = `00:0${Math.floor(sec)} / 00:0${Math.floor(totalSec)}`;
        // 動態展示 105 × 20 = 2100
        const d1 = document.getElementById('anim-1-d1');
        const d2 = document.getElementById('anim-1-d2');
        const d3 = document.getElementById('anim-1-d3');
        const d4 = document.getElementById('anim-1-d4');
        const tensDigit = document.getElementById('anim-1-tens-digit');

        if (p < 20) {
          if (tensDigit) tensDigit.style.transform = 'scale(1)';
          if (d1) d1.style.opacity = '0';
          if (d2) d2.style.opacity = '0';
          if (d3) d3.style.opacity = '0';
          if (d4) d4.style.opacity = '0';
        } else if (p < 50) {
          if (tensDigit) tensDigit.style.transform = 'scale(1.3)';
          if (d3) d3.style.opacity = '1'; // 0 出現在十位
          if (d4) d4.style.opacity = '0.3';
        } else if (p < 80) {
          if (d2) d2.style.opacity = '1'; // 1 出現在百位
          if (d3) d3.style.opacity = '1';
        } else {
          if (d1) d1.style.opacity = '1'; // 2 出現在千位
          if (d2) d2.style.opacity = '1';
          if (d3) d3.style.opacity = '1';
          if (d4) d4.style.opacity = '0.7';
        }
      } else if (id === 2) {
        // 四位數乘二位數逐步動畫
        const rowL1 = document.getElementById('anim-2-row-layer1');
        const rowL2 = document.getElementById('anim-2-row-layer2');
        const rowSum = document.getElementById('anim-2-row-sum');

        if (p < 30) {
          if (status) status.textContent = '步驟 1: 個位乘法';
          if (rowL1) rowL1.style.opacity = '1';
          if (rowL2) rowL2.style.opacity = '0.15';
          if (rowSum) rowSum.style.opacity = '0.15';
        } else if (p < 70) {
          if (status) status.textContent = '步驟 2: 十位向左移位';
          if (rowL1) rowL1.style.opacity = '1';
          if (rowL2) rowL2.style.opacity = '1';
          if (rowSum) rowSum.style.opacity = '0.15';
        } else {
          if (status) status.textContent = '步驟 3: 兩層相加';
          if (rowL1) rowL1.style.opacity = '1';
          if (rowL2) rowL2.style.opacity = '1';
          if (rowSum) rowSum.style.opacity = '1';
        }
      } else if (id === 3) {
        // 迷思天秤動態
        const beam = document.getElementById('anim-3-beam');
        const caption = document.getElementById('anim-3-caption');
        // p 從 0 到 100，天秤向右傾斜（右重左輕）
        const angle = (p / 100) * 18; // 傾斜度數
        if (beam) {
          beam.style.transform = `rotate(${angle}deg)`;
        }
        if (p > 50) {
          if (caption) caption.textContent = `❌ 錯誤 12,048 vs ✔ 正確 48,192（差了 36,144！）`;
        }
      }
    }

    // 初始化第一頁
    updateDeckUI();
  </script>
</body>
</html>
"""

for fname in ["index.html", "乘法.html"]:
    fpath = Path(r"d:\antui\動畫簡報") / fname
    text = fpath.read_text(encoding="utf-8")
    split_marker = "  <!-- =========================================="
    parts = text.split(split_marker)
    # 取前面直到最後一個區塊
    base_html = parts[0] + split_marker + parts[1] # 保留 HTML 本體直到主標記
    # 找到 </body> 前的最後註解
    script_idx = text.rfind("  <!-- ==========================================\n       現代簡報與三大關鍵動畫核心控制器")
    if script_idx != -1:
        new_text = text[:script_idx] + script_content.strip() + "\n"
        fpath.write_text(new_text, encoding="utf-8")
        print(f"Updated {fname} script block successfully!")
