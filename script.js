/**
 * DUN-YUAN AI / antui - Main Application Script
 * Dynamic data rendering, live search & filtering, dual-theme switching,
 * interactive SKILL.md modal viewer, and clipboard toast system.
 */

// 全域狀態
let siteData = null;
let currentCategoryFilter = 'ALL';
let currentSearchQuery = '';

// DOM 載入後初始化
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initHamburger();
  loadSiteData();
  setupSearchEvents();
  setupModalEvents();
});

/* --------------------------------------------------------------------------
   主題切換 (Light / Dark Theme)
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('dun_theme') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  setTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
      localStorage.setItem('dun_theme', next);
    });
  }
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  document.body.setAttribute('data-theme', theme);
  const toggleBtn = document.getElementById('themeToggle');
  if (toggleBtn) {
    const icon = toggleBtn.querySelector('.theme-toggle-icon');
    const text = toggleBtn.querySelector('.theme-toggle-text');
    if (theme === 'dark') {
      if (icon) icon.textContent = '☀️';
      if (text) text.textContent = '日間模式';
    } else {
      if (icon) icon.textContent = '☾';
      if (text) text.textContent = '夜間模式';
    }
  }
}

/* --------------------------------------------------------------------------
   手機版選單 (Hamburger Menu)
   -------------------------------------------------------------------------- */
function initHamburger() {
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const navMenu = document.getElementById('navMenu');

  if (hamburgerBtn && navMenu) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      navMenu.classList.toggle('open');
      const expanded = navMenu.classList.contains('open');
      hamburgerBtn.setAttribute('aria-expanded', expanded);
    });

    // 點擊導覽連結後平滑捲動並關閉選單（精準扣除 sticky header 高度）
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        navMenu.classList.remove('open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');

        if (href && href.startsWith('#')) {
          const targetEl = document.querySelector(href);
          if (targetEl) {
            e.preventDefault();
            const headerOffset = 80;
            const elementPosition = targetEl.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            window.scrollTo({
              top: offsetPosition,
              behavior: 'smooth'
            });
          }
        }
      });
    });

    // 點擊外側空白處自動關閉手機選單
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !hamburgerBtn.contains(e.target) && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }
}

/* --------------------------------------------------------------------------
   載入資料 (Load data.json)
   -------------------------------------------------------------------------- */
async function loadSiteData() {
  try {
    const res = await fetch('data.json?v=2.0');
    if (!res.ok) throw new Error('Failed to load data.json');
    siteData = await res.json();

    renderPageInfo(siteData.pageInfo);
    renderStats(siteData.stats);
    renderFeaturedSkills(siteData.skills);
    renderFilterPills(siteData.projects_by_category);
    renderSkillsCatalog(siteData.projects_by_category);
    renderWorks(siteData.works);
    renderExperiences(siteData.experiences);

    // 頁尾統計
    const totalCountElem = document.getElementById('footerTotalSkills');
    if (totalCountElem) {
      totalCountElem.textContent = siteData.skills.length;
    }
  } catch (err) {
    console.error('Error loading data:', err);
    const container = document.getElementById('skills-container');
    if (container) {
      container.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--accent-orange-dark);">
        ⚠️ 載入技能資料失敗，請確認 data.json 檔案是否存在。
      </div>`;
    }
  }
}

/* --------------------------------------------------------------------------
   渲染頁面資訊與統計
   -------------------------------------------------------------------------- */
function renderPageInfo(info) {
  if (!info) return;
  const ownerNameElems = document.querySelectorAll('.author-name-text');
  ownerNameElems.forEach(el => el.textContent = info.ownerName);

  const bioElem = document.getElementById('authorBio');
  if (bioElem) bioElem.textContent = info.bio;

  const titleElem = document.getElementById('authorJobTitle');
  if (titleElem) titleElem.textContent = info.jobTitle;

  const emailBtn = document.getElementById('authorEmailBtn');
  if (emailBtn) {
    emailBtn.onclick = () => {
      copyToClipboard(info.email, '✅ 已複製電子信箱：' + info.email);
    };
  }
}

function renderStats(stats) {
  const container = document.getElementById('stats-grid');
  if (!container || !stats) return;

  container.innerHTML = stats.map(s => `
    <div class="stat-card">
      <div class="stat-icon">${s.icon || '🚀'}</div>
      <div class="stat-number">${escapeHtml(s.number)}</div>
      <div class="stat-label">${escapeHtml(s.label)}</div>
    </div>
  `).join('');
}

/* --------------------------------------------------------------------------
   渲染精選技能 (Featured Skills)
   -------------------------------------------------------------------------- */
function renderFeaturedSkills(skills) {
  const container = document.getElementById('featured-skills-grid');
  if (!container || !skills) return;

  const featured = skills.filter(s => s.showOnMain).slice(0, 6);
  container.innerHTML = featured.map(s => renderSkillCardHtml(s)).join('');
}

/* --------------------------------------------------------------------------
   渲染類別快速導覽 Pills
   -------------------------------------------------------------------------- */
function renderFilterPills(categories) {
  const container = document.getElementById('categoryQuickNav');
  if (!container || !categories) return;

  let html = `<button type="button" class="pill-btn active" data-category="ALL">全部 (${siteData.skills.length})</button>`;
  
  categories.forEach(cat => {
    // 擷取簡短標籤名稱
    const shortName = cat.category.replace(/^[^\w\s\u4e00-\u9fa5]+/, '').trim();
    html += `<button type="button" class="pill-btn" data-category="${escapeHtml(cat.category)}">${escapeHtml(shortName)} (${cat.count})</button>`;
  });

  container.innerHTML = html;

  container.querySelectorAll('.pill-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const cat = btn.getAttribute('data-category');
      filterByCategory(cat, true);
    });
  });
}

/* --------------------------------------------------------------------------
   渲染完整技能目錄 (Full Skills Catalog)
   -------------------------------------------------------------------------- */
function renderSkillsCatalog(categories) {
  const container = document.getElementById('skills-container');
  if (!container || !categories) return;

  const query = currentSearchQuery.trim().toLowerCase();
  let totalVisible = 0;
  let html = '';

  // 搜尋或特定類別篩選時，暫時隱藏頂部固定精選區塊，直接將符合結果呈現在最上方
  const featuredSection = document.getElementById('featured');
  if (featuredSection) {
    const isFiltering = Boolean(query || currentCategoryFilter !== 'ALL');
    featuredSection.style.display = isFiltering ? 'none' : '';
  }

  categories.forEach((cat, idx) => {
    // 篩選當前類別
    if (currentCategoryFilter !== 'ALL' && cat.category !== currentCategoryFilter) {
      return;
    }

    // 篩選搜尋字詞
    const filteredItems = cat.items.filter(item => {
      if (!query) return true;
      const haystack = (
        item.name + ' ' +
        item.friendly_name + ' ' +
        item.description + ' ' +
        item.full_description + ' ' +
        item.category + ' ' +
        item.triggers.join(' ')
      ).toLowerCase();
      return haystack.includes(query);
    });

    if (filteredItems.length > 0) {
      totalVisible += filteredItems.length;
      html += `
        <div class="category-block" id="cat-block-${idx}">
          <div class="category-title-bar">
            <h3 class="category-title">
              <span>${escapeHtml(cat.category)}</span>
            </h3>
            <span class="category-count">${filteredItems.length} 款技能</span>
          </div>
          <div class="cards-grid">
            ${filteredItems.map(item => renderSkillCardHtml(item)).join('')}
          </div>
        </div>
      `;
    }
  });

  if (totalVisible === 0) {
    html = `
      <div style="text-align: center; padding: 60px 20px; color: var(--page-muted);">
        <div style="font-size: 3rem; margin-bottom: 12px;">🔍</div>
        <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 8px;">未找到符合「${escapeHtml(query)}」的技能</h3>
        <p style="font-size: 0.95rem;">請嘗試不同關鍵字，或點擊下方按鈕重置搜尋。</p>
        <button class="btn-primary" style="margin-top: 16px; display: inline-flex;" onclick="resetSearch()">重設搜尋條件</button>
      </div>
    `;
  }

  container.innerHTML = html;

  // 更新搜尋狀態列計數
  const searchCountBadge = document.getElementById('searchCountBadge');
  if (searchCountBadge) {
    searchCountBadge.textContent = query || currentCategoryFilter !== 'ALL' 
      ? `已篩選顯示 ${totalVisible} 款技能 (共 ${siteData.skills.length} 款)`
      : `收錄共 ${siteData.skills.length} 款全域 AntiGravity 技能`;
  }
}

/* 單張 Skill 卡片 HTML */
function renderSkillCardHtml(item) {
  const triggerPills = item.triggers && item.triggers.length > 0
    ? item.triggers.slice(0, 4).map(t => `
        <span class="trigger-pill" onclick="copyTrigger('${escapeJsString(t)}')" title="點擊複製觸發語">
          「${escapeHtml(t)}」
        </span>
      `).join('')
    : '<span style="font-size:0.75rem; color:var(--page-muted);">（依需求直接對話載入）</span>';

  const primaryTrigger = item.triggers && item.triggers.length > 0 ? item.triggers[0] : item.name;

  const coverHtml = item.image 
    ? `<div class="card-cover">
         <img src="${item.image}" alt="${escapeHtml(item.friendly_name || item.name)}" loading="lazy">
       </div>`
    : `<div class="card-cover-fallback">
         <span class="fallback-icon">${item.icon || '⚡'}</span>
       </div>`;

  return `
    <div class="skill-card">
      ${coverHtml}
      <div class="card-top">
        <div class="card-icon-title">
          <span class="card-icon">${item.icon || '⚡'}</span>
          <div>
            <h4 class="card-title">${escapeHtml(item.friendly_name || item.name)}</h4>
          </div>
        </div>
        <span class="badge-tag">${escapeHtml(item.badge || '全域技能')}</span>
      </div>

      <div class="card-code-id">${escapeHtml(item.name)}</div>
      <p class="card-desc">${escapeHtml(item.description)}</p>

      <div class="triggers-wrap">
        <div class="triggers-title">
          <span>🎯 常用觸發語句：</span>
        </div>
        <div class="trigger-pills">
          ${triggerPills}
        </div>
      </div>

      <div class="card-actions">
        <button type="button" class="btn-primary" onclick="openSkillModal('${escapeJsString(item.id)}')">
          <span>📖 查看完整說明</span>
        </button>
        <button type="button" class="btn-outline" onclick="copyTrigger('${escapeJsString(primaryTrigger)}')" title="一鍵複製觸發提示詞">
          <span>📋 複製</span>
        </button>
        <a href="https://github.com/asc103138/dotfiles/tree/main/private_dot_gemini/config/skills/${encodeURIComponent(item.folder)}" 
           target="_blank" rel="noopener noreferrer" class="btn-outline" title="前往 GitHub 檢視檔案">
          <span>🐙</span>
        </a>
      </div>
    </div>
  `;
}

/* --------------------------------------------------------------------------
   搜尋與篩選邏輯
   -------------------------------------------------------------------------- */
function setupSearchEvents() {
  const input = document.getElementById('toolSearchInput');
  const clearBtn = document.getElementById('toolSearchClearBtn');

  if (input) {
    input.addEventListener('input', (e) => {
      currentSearchQuery = e.target.value;
      if (clearBtn) {
        clearBtn.style.display = currentSearchQuery ? 'flex' : 'none';
      }
      // 輸入關鍵字時自動切回全局搜尋，避免類別篩選衝突
      if (currentSearchQuery.trim()) {
        currentCategoryFilter = 'ALL';
        document.querySelectorAll('#categoryQuickNav .pill-btn').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-category') === 'ALL');
        });
      }
      renderSkillsCatalog(siteData.projects_by_category);
    });

    // 行動載具按 Enter/搜尋後自動收起鍵盤並平滑捲動至目錄區
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        input.blur();
        scrollToSkillsSection();
      }
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      resetSearch();
    });
  }

  // 熱門關鍵字按鈕點擊
  document.querySelectorAll('.hot-keyword-pill').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelectorAll('.hot-keyword-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      btn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });

      // 切換熱門關鍵字時重設類別為全部
      currentCategoryFilter = 'ALL';
      document.querySelectorAll('#categoryQuickNav .pill-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-category') === 'ALL');
      });

      const keyword = btn.getAttribute('data-keyword') || '';
      if (input) {
        input.value = keyword;
        currentSearchQuery = keyword;
        if (clearBtn) clearBtn.style.display = keyword ? 'flex' : 'none';
      }
      renderSkillsCatalog(siteData.projects_by_category);
      if (keyword) {
        scrollToSkillsSection();
      }
    });
  });
}

function scrollToSkillsSection() {
  const target = document.getElementById('skills');
  if (target) {
    const headerOffset = 85;
    const elementPosition = target.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

function filterByCategory(category, autoScroll = true) {
  currentCategoryFilter = category;

  // 切換特定分類時清空搜尋字串與熱門關鍵字，避免交互衝突
  const input = document.getElementById('toolSearchInput');
  const clearBtn = document.getElementById('toolSearchClearBtn');
  if (input) input.value = '';
  if (clearBtn) clearBtn.style.display = 'none';
  currentSearchQuery = '';
  document.querySelectorAll('.hot-keyword-pill').forEach(b => b.classList.remove('active'));
  const firstHot = document.querySelector('.hot-keyword-pill');
  if (firstHot) firstHot.classList.add('active');

  document.querySelectorAll('#categoryQuickNav .pill-btn').forEach(btn => {
    const isMatch = btn.getAttribute('data-category') === category;
    btn.classList.toggle('active', isMatch);
    if (isMatch) {
      btn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  });

  renderSkillsCatalog(siteData.projects_by_category);

  if (autoScroll) {
    scrollToSkillsSection();
  }
}

function resetSearch() {
  const input = document.getElementById('toolSearchInput');
  const clearBtn = document.getElementById('toolSearchClearBtn');
  if (input) input.value = '';
  if (clearBtn) clearBtn.style.display = 'none';
  currentSearchQuery = '';
  currentCategoryFilter = 'ALL';
  document.querySelectorAll('.hot-keyword-pill').forEach(b => b.classList.remove('active'));
  const firstHot = document.querySelector('.hot-keyword-pill');
  if (firstHot) firstHot.classList.add('active');
  document.querySelectorAll('#categoryQuickNav .pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-category') === 'ALL');
  });
  renderSkillsCatalog(siteData.projects_by_category);
}

/* --------------------------------------------------------------------------
   渲染專案成果與經歷 (Works & Experiences)
   -------------------------------------------------------------------------- */
function renderWorks(works) {
  const container = document.getElementById('works-container');
  if (!container || !works) return;

  container.innerHTML = works.map(w => {
    let actionBtns = '';
    if (w.demoLink) {
      actionBtns += `<a href="${escapeHtml(w.demoLink)}" target="_blank" class="btn-primary" style="font-size:0.8rem; padding: 6px 14px; margin-top: 12px; display: inline-flex; align-items:center; gap: 6px; text-decoration: none; border-radius: var(--radius-sm); font-weight: 600;"><span>🚀 線上實戰體驗</span></a> `;
    }
    if (w.link) {
      actionBtns += `<a href="${escapeHtml(w.link)}" target="_blank" class="btn-outline" style="font-size:0.8rem; padding: 6px 14px; margin-top: 12px; display: inline-flex; align-items:center; gap: 6px; text-decoration: none; border-radius: var(--radius-sm); font-weight: 600;"><span>📁 查看專案庫</span></a>`;
    }

    return `
      <div class="work-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="work-tag">${escapeHtml(w.tag || '實務作品')}</span>
          <span style="font-size:0.8rem; color:var(--page-muted);">${escapeHtml(w.date || '')}</span>
        </div>
        <h4 class="work-title">${escapeHtml(w.title)}</h4>
        <p class="work-desc">${escapeHtml(w.desc)}</p>
        ${actionBtns ? `<div style="display:flex; gap:8px; flex-wrap:wrap;">${actionBtns}</div>` : ''}
      </div>
    `;
  }).join('');
}

function renderExperiences(exps) {
  const container = document.getElementById('experiences-container');
  if (!container || !exps) return;

  container.innerHTML = exps.map(e => `
    <div class="stat-card" style="text-align: left; padding: 18px;">
      <div style="display:flex; justify-content:space-between; margin-bottom: 6px;">
        <span class="badge-tag">${escapeHtml(e.type || '實務')}</span>
        <span style="font-size:0.85rem; color:var(--page-muted);">${escapeHtml(e.date)}</span>
      </div>
      <h4 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 4px;">${escapeHtml(e.school)}</h4>
      <p style="font-size: 0.9rem; color: var(--page-muted); line-height: 1.5;">${escapeHtml(e.topic)}</p>
    </div>
  `).join('');
}

/* --------------------------------------------------------------------------
   SKILL.md 內文彈窗閱讀器 (Modal Viewer)
   -------------------------------------------------------------------------- */
function setupModalEvents() {
  const overlay = document.getElementById('skillModalOverlay');
  const closeBtn = document.getElementById('modalCloseBtn');
  const footerCloseBtn = document.getElementById('modalFooterCloseBtn');

  if (closeBtn) closeBtn.addEventListener('click', closeSkillModal);
  if (footerCloseBtn) footerCloseBtn.addEventListener('click', closeSkillModal);

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeSkillModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSkillModal();
  });
}

let activeModalSkill = null;

function openSkillModal(skillId) {
  if (!siteData) return;
  const skill = siteData.skills.find(s => s.id === skillId);
  if (!skill) return;

  activeModalSkill = skill;

  const overlay = document.getElementById('skillModalOverlay');
  const titleElem = document.getElementById('modalSkillTitle');
  const categoryElem = document.getElementById('modalSkillCategory');
  const bodyElem = document.getElementById('modalSkillBody');

  if (titleElem) titleElem.textContent = (skill.icon ? skill.icon + ' ' : '') + (skill.friendly_name || skill.name);
  if (categoryElem) categoryElem.textContent = skill.category;

  if (bodyElem) {
    const renderedHtml = renderMarkdown(skill.doc_content || skill.full_description);
    bodyElem.innerHTML = `
      <div style="background: var(--page-bg); border: 1px solid var(--page-border); border-radius: var(--radius-sm); padding: 14px 18px; margin-bottom: 20px;">
        <div style="font-size: 0.85rem; color: var(--page-muted); margin-bottom: 4px;">識別名稱：<code>${escapeHtml(skill.name)}</code></div>
        <div style="font-size: 0.85rem; color: var(--page-muted);">所屬路徑：<code>${escapeHtml(skill.folder)}/SKILL.md</code></div>
      </div>
      <div class="markdown-body">
        ${renderedHtml}
      </div>
    `;
  }

  if (overlay) {
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeSkillModal() {
  const overlay = document.getElementById('skillModalOverlay');
  if (overlay) {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
  activeModalSkill = null;
}

function copyActiveModalSkill() {
  if (!activeModalSkill) return;
  const content = `# ${activeModalSkill.friendly_name}\n\n${activeModalSkill.doc_content}`;
  copyToClipboard(content, '✅ 已複製整篇 Skill 指引與規格！');
}

/* 輕量級 Markdown 格式化引擎 (免外部相依) */
function renderMarkdown(md) {
  if (!md) return '';

  let html = md
    // 跳脫 HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // 程式碼區塊 (Code blocks)
    .replace(/```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre><code>${code.trim()}</code></pre>`;
    })
    // 標題 (Headings)
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // 引用塊 (Blockquotes)
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    // 粗體與斜體 (Bold & Italic)
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    // 行內程式碼 (Inline code)
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    // 無序清單 (Unordered lists)
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>')
    .replace(/<\/ul>\s*<ul>/gim, '')
    // 換行轉段落 (Paragraphs)
    .split(/\n\n+/)
    .map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<h') || p.startsWith('<pre') || p.startsWith('<ul') || p.startsWith('<blockquote')) {
        return p;
      }
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    })
    .join('');

  return html;
}

/* --------------------------------------------------------------------------
   剪貼簿與 Toast 通知 (Clipboard & Toast)
   -------------------------------------------------------------------------- */
function copyTrigger(text) {
  const clean = text.replace(/^[「『]/, '').replace(/[」』]$/, '').trim();
  copyToClipboard(clean, `✅ 已複製觸發語：「${clean}」`);
}

function copyToClipboard(text, successMsg) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg || '✅ 已複製到剪貼簿！');
    }).catch(() => {
      fallbackCopyText(text, successMsg);
    });
  } else {
    fallbackCopyText(text, successMsg);
  }
}

function fallbackCopyText(text, successMsg) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.top = '-9999px';
  textArea.style.left = '-9999px';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    showToast(successMsg || '✅ 已複製到剪貼簿！');
  } catch (err) {
    console.error('Fallback copy failed', err);
    showToast('⚠️ 複製失敗，請手動反白複製。');
  }
  document.body.removeChild(textArea);
}

let toastTimer = null;
function showToast(message) {
  let toast = document.getElementById('siteToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'siteToast';
    toast.className = 'toast-msg';
    document.body.appendChild(toast);
  }

  toast.innerHTML = message;
  toast.classList.add('show');

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove('show');
  }, 2200);
}

/* 輔助函式 */
function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[m]);
}

function escapeJsString(str) {
  return String(str || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
}
