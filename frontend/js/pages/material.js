// Study-material pages (python-material.html, c-material.html, etc.):
// W3Schools-inspired learning interface:
// - Top language/tutorial switcher bar (Java, JavaScript, DSA, Data Science, Machine Learning, Deep Learning, AI,
//   Generative AI, Agentic AI, Python, NumPy, Pandas, Matplotlib, Seaborn, Statistics, Excel,
//   Power BI, C, C++, HTML, CSS, SQL, Django, FastAPI)
// - Left sidebar with ALL headings in the left side corner
// - Clicking any heading displays ALL context on the right side
// - Previous / Next navigation controls at top & bottom
// - Subtopics navigation under active module
// - Real-time heading filter search in sidebar
// - Responsive mobile off-canvas drawer
import { page, setTitle } from "../ui.js";

const TUTORIALS = [
  { slug: "java", file: "java-material.html", name: "Java", emoji: "☕" },
  { slug: "javascript", file: "javascript-material.html", name: "JavaScript", emoji: "🟨" },
  { slug: "dsa", file: "dsa-material.html", name: "DSA", emoji: "🧠" },
  { slug: "dbms", file: "dbms-material.html", name: "DBMS", emoji: "🗄️" },
  { slug: "aptitude", file: "aptitude-material.html", name: "Aptitude", emoji: "🧠" },
  { slug: "data-science", file: "data-science-material.html", name: "Data Science", emoji: "📊" },
  { slug: "machine-learning", file: "machine-learning-material.html", name: "Machine Learning", emoji: "🤖" },
  { slug: "deep-learning", file: "deep-learning-material.html", name: "Deep Learning", emoji: "🧠" },
  { slug: "ai", file: "ai-material.html", name: "AI", emoji: "✨" },
  { slug: "generative-ai", file: "generative-ai-material.html", name: "Generative AI", emoji: "🪄" },
  { slug: "agentic-ai", file: "agentic-ai-material.html", name: "Agentic AI", emoji: "🧭" },
  { slug: "python", file: "python-material.html", name: "Python", emoji: "🐍" },
  { slug: "numpy", file: "numpy-material.html", name: "NumPy", emoji: "🔢" },
  { slug: "pandas", file: "pandas-material.html", name: "Pandas", emoji: "🐼" },
  { slug: "matplotlib", file: "matplotlib-material.html", name: "Matplotlib", emoji: "📈" },
  { slug: "seaborn", file: "seaborn-material.html", name: "Seaborn", emoji: "🌊" },
  { slug: "statistics", file: "statistics-material.html", name: "Statistics", emoji: "🧮" },
  { slug: "excel", file: "excel-material.html", name: "Excel", emoji: "📗" },
  { slug: "power-bi", file: "power-bi-material.html", name: "Power BI", emoji: "🔶" },
  { slug: "c", file: "c-material.html", name: "C", emoji: "💻" },
  { slug: "cpp", file: "cpp-material.html", name: "C++", emoji: "⚙️" },
  { slug: "html", file: "html-material.html", name: "HTML", emoji: "🌐" },
  { slug: "css", file: "css-material.html", name: "CSS", emoji: "🎨" },
  { slug: "sql", file: "sql-material.html", name: "SQL", emoji: "🗃️" },
  { slug: "django", file: "django-material.html", name: "Django", emoji: "🌿" },
  { slug: "fastapi", file: "fastapi-material.html", name: "FastAPI", emoji: "⚡" },
];

page(async (app) => {
  const currentPath = location.pathname.split("/").pop() || "python-material.html";
  const currentTutorial = TUTORIALS.find((t) => t.file.toLowerCase() === currentPath.toLowerCase()) || {
    name: "Tutorial",
    emoji: "📚",
    file: currentPath,
  };

  const rawH1 = app.querySelector("h1")?.textContent?.trim() || "";
  const pageTitle = rawH1.replace(/^[^\w\s]+/, "").trim() || `${currentTutorial.name} Complete Material`;
  setTitle(pageTitle);

  // Collect module cards
  const cards = [...app.querySelectorAll(".module-card")];
  if (!cards.length) return;

  // Extract stats items from hero if present
  const statItems = [...app.querySelectorAll(".pm-hero .stat")].map((el) => {
    const num = el.querySelector(".stat-num")?.textContent?.trim() || "";
    const lbl = el.querySelector(".stat-lbl")?.textContent?.trim() || "";
    return { num, lbl };
  });

  // Extract module metadata and subtopics from cards
  const modules = cards.map((card, idx) => {
    const id = card.id || `m${idx + 1}`;
    card.id = id;
    const emoji = card.querySelector(".module-emoji")?.textContent?.trim() || currentTutorial.emoji;
    const h2Text = card.querySelector(".module-title-group h2")?.textContent?.trim() || `Module ${idx + 1}`;
    const subText = card.querySelector(".module-title-group p")?.textContent?.trim() || "";
    const headingClean = h2Text.replace(/^Module\s*\d+\s*[—–-]\s*/i, "").trim() || h2Text;
    const shortTitle = `${idx + 1} · ${headingClean}`;

    // Extract subtopics for sidebar navigation
    const subtopics = [...card.querySelectorAll(".topic h3, .interview-box strong")].map((el, sIdx) => {
      const topicId = `${id}-sub-${sIdx}`;
      el.id = topicId;
      const rawText = el.textContent.trim();
      const cleanSub = rawText.replace(/^[^\w\s]+/, "").trim() || rawText;
      return { id: topicId, title: cleanSub, rawText };
    });

    return { id, emoji, fullTitle: h2Text, headingClean, shortTitle, sub: subText, index: idx, card, subtopics };
  });

  // Clean up any existing generated elements if re-rendered
  app.querySelector(".w3-subnav")?.remove();
  app.querySelector(".w3-container")?.remove();

  // Hide the legacy hero, pill nav, and expand/collapse tools
  const oldHero = app.querySelector(".pm-hero");
  if (oldHero) oldHero.style.display = "none";
  const oldNav = app.querySelector(".module-nav");
  if (oldNav) oldNav.style.display = "none";
  const oldTools = app.querySelector(".pm-tools");
  if (oldTools) oldTools.style.display = "none";

  // Build the Top Tutorial Subnav (W3Schools Subjects Bar)
  const subnav = document.createElement("nav");
  subnav.className = "w3-subnav";
  subnav.setAttribute("aria-label", "Tutorial Subjects");
  subnav.innerHTML = `
    <div class="w3-subnav-scroll">
      ${TUTORIALS.map((t) => {
        const isActive = currentPath.toLowerCase().includes(t.file.toLowerCase()) || currentPath.toLowerCase().startsWith(t.slug + "-");
        return `<a href="${t.file}" class="w3-subnav-link ${isActive ? "active" : ""}">${t.emoji} ${t.name}</a>`;
      }).join("")}
      <a href="study.html" class="w3-subnav-link w3-subnav-all">📚 All Study Materials</a>
    </div>
  `;
  app.prepend(subnav);

  // Build W3Schools 2-Column Container (Full Width, Left-Corner Docked)
  const container = document.createElement("div");
  container.className = "w3-container";

  // Left Sidebar: Pinned to the Left Side Corner
  const sidebar = document.createElement("aside");
  sidebar.className = "w3-sidebar";
  sidebar.id = "w3-sidebar";
  sidebar.innerHTML = `
    <div class="w3-sidebar-header">
      <div class="w3-sidebar-title-row">
        <span class="w3-sidebar-icon">${currentTutorial.emoji}</span>
        <h2 class="w3-sidebar-title">${currentTutorial.name.toUpperCase()} TUTORIAL</h2>
        <button class="w3-sidebar-close" id="w3-sidebar-close" aria-label="Close menu">✕</button>
      </div>
      <div class="w3-search-box">
        <span class="w3-search-icon">🔍</span>
        <input type="search" id="w3-module-search" class="w3-search-input" placeholder="Filter headings..." aria-label="Filter headings">
      </div>
    </div>
    <div class="w3-sidebar-list" id="w3-sidebar-list" role="navigation" aria-label="All Headings">
      ${modules.map((m) => `
        <div class="w3-heading-group" data-id="${m.id}" id="group-${m.id}">
          <a href="#${m.id}" class="w3-sidebar-item" data-id="${m.id}" id="nav-${m.id}" title="${m.headingClean}">
            <span class="w3-item-title">${m.shortTitle}</span>
            <span class="w3-item-arrow">›</span>
          </a>
          <div class="w3-subtopics" id="subtopics-${m.id}" style="display: none;">
            ${m.subtopics.map((st) => `
              <a href="#${st.id}" class="w3-subtopic-link" data-sub-id="${st.id}">
                ${st.title}
              </a>
            `).join("")}
          </div>
        </div>
      `).join("")}
    </div>
  `;

  // Backdrop overlay for mobile drawer
  const overlay = document.createElement("div");
  overlay.className = "w3-overlay";
  overlay.id = "w3-overlay";

  // Right Content Pane: Displays ALL Context on the Right Side
  const mainPane = document.createElement("section");
  mainPane.className = "w3-main-pane";
  mainPane.id = "w3-main-pane";

  // Mobile Top Bar
  const mobileBar = document.createElement("div");
  mobileBar.className = "w3-mobile-bar";
  mobileBar.innerHTML = `
    <button class="w3-mobile-menu-btn" id="w3-open-sidebar">
      <span class="menu-icon">☰</span>
      <span class="menu-text">Headings</span>
      <span class="w3-mobile-badge" id="w3-mobile-badge">1 / ${modules.length}</span>
    </button>
    <div class="w3-mobile-arrows">
      <button class="w3-mobile-arrow-btn" id="w3-m-prev" title="Previous module">❮ Prev</button>
      <button class="w3-mobile-arrow-btn" id="w3-m-next" title="Next module">Next ❯</button>
    </div>
  `;
  mainPane.append(mobileBar);

  // Top Nav Bar (< Previous, Next >)
  const topNav = document.createElement("div");
  topNav.className = "w3-nav-bar top-nav";
  topNav.innerHTML = `
    <button class="w3-nav-btn prev-btn" id="w3-prev-top">❮ Previous</button>
    <div class="w3-nav-center">
      <span class="w3-counter" id="w3-counter">Module 1 of ${modules.length}</span>
    </div>
    <button class="w3-nav-btn next-btn" id="w3-next-top">Next ❯</button>
  `;
  mainPane.append(topNav);

  // Compact Stats Banner (overview pills)
  if (statItems.length) {
    const statsBanner = document.createElement("div");
    statsBanner.className = "w3-stats-banner";
    statsBanner.innerHTML = `
      <div class="w3-stats-list">
        <span class="w3-stats-badge">${currentTutorial.emoji} ${pageTitle}</span>
        ${statItems.map((s) => `<span class="w3-stat-chip"><strong>${s.num}</strong> ${s.lbl}</span>`).join("")}
      </div>
      <a href="study.html" class="w3-stats-link">← All study materials</a>
    `;
    mainPane.append(statsBanner);
  }

  // Content Area wrapper
  const contentArea = document.createElement("div");
  contentArea.className = "w3-content-area";

  // Move each module card into contentArea
  modules.forEach((m) => {
    m.card.classList.add("w3-module-view");
    const body = m.card.querySelector(".module-body");
    if (body) body.classList.add("open");

    const toggle = m.card.querySelector(".module-toggle");
    if (toggle) toggle.style.display = "none";

    contentArea.append(m.card);
  });
  mainPane.append(contentArea);

  // Bottom Nav Bar with descriptive next/prev titles
  const bottomNav = document.createElement("div");
  bottomNav.className = "w3-nav-bar bottom-nav";
  bottomNav.innerHTML = `
    <button class="w3-nav-btn prev-btn" id="w3-prev-bottom">❮ Previous</button>
    <a href="#app" class="w3-back-to-top" id="w3-top-link">▲ Top</a>
    <button class="w3-nav-btn next-btn" id="w3-next-bottom">Next ❯</button>
  `;
  mainPane.append(bottomNav);

  container.append(sidebar, overlay, mainPane);

  // Replace old pm-content in app
  const oldContent = app.querySelector(".pm-content");
  if (oldContent) {
    oldContent.replaceWith(container);
  } else {
    app.append(container);
  }

  // Active module switching state
  let currentIdx = 0;

  function setDrawerOpen(open) {
    sidebar.classList.toggle("drawer-open", open);
    overlay.classList.toggle("drawer-open", open);
    document.body.style.overflow = open && window.innerWidth <= 960 ? "hidden" : "";
  }

  function showModule(index, updateHash = true, shouldScroll = true) {
    if (index < 0) index = 0;
    if (index >= modules.length) index = modules.length - 1;
    currentIdx = index;
    const mod = modules[index];

    // Show ONLY the active module on the right side, hide all other modules!
    modules.forEach((m, i) => {
      if (i === index) {
        m.card.classList.add("w3-active");
        m.card.style.display = "block";
      } else {
        m.card.classList.remove("w3-active");
        m.card.style.display = "none";
      }
    });

    // Update active state and subtopics in left sidebar
    modules.forEach((m, i) => {
      const isAct = i === index;
      const navItem = sidebar.querySelector(`#nav-${m.id}`);
      const subBox = sidebar.querySelector(`#subtopics-${m.id}`);
      if (navItem) navItem.classList.toggle("active", isAct);
      if (subBox) subBox.style.display = isAct && m.subtopics.length ? "block" : "none";
      if (isAct && navItem) {
        navItem.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    });

    // Update Top & Bottom Nav controls
    const isFirst = index === 0;
    const isLast = index === modules.length - 1;

    const prevTop = topNav.querySelector("#w3-prev-top");
    const nextTop = topNav.querySelector("#w3-next-top");
    const prevBottom = bottomNav.querySelector("#w3-prev-bottom");
    const nextBottom = bottomNav.querySelector("#w3-next-bottom");
    const mPrev = mobileBar.querySelector("#w3-m-prev");
    const mNext = mobileBar.querySelector("#w3-m-next");

    prevTop.disabled = isFirst;
    mPrev.disabled = isFirst;
    prevTop.style.opacity = isFirst ? "0.4" : "1";
    prevTop.style.pointerEvents = isFirst ? "none" : "auto";
    mPrev.style.opacity = isFirst ? "0.4" : "1";
    mPrev.style.pointerEvents = isFirst ? "none" : "auto";

    nextTop.disabled = isLast;
    mNext.disabled = isLast;
    nextTop.style.opacity = isLast ? "0.4" : "1";
    nextTop.style.pointerEvents = isLast ? "none" : "auto";
    mNext.style.opacity = isLast ? "0.4" : "1";
    mNext.style.pointerEvents = isLast ? "none" : "auto";

    // Text for bottom buttons: descriptive titles
    if (!isFirst) {
      const prevMod = modules[index - 1];
      prevBottom.textContent = `❮ Prev: ${prevMod.headingClean.slice(0, 22)}${prevMod.headingClean.length > 22 ? "…" : ""}`;
      prevBottom.style.visibility = "visible";
    } else {
      prevBottom.textContent = "❮ Previous";
      prevBottom.style.visibility = "hidden";
    }

    if (!isLast) {
      const nextMod = modules[index + 1];
      nextBottom.textContent = `Next: ${nextMod.headingClean.slice(0, 22)}${nextMod.headingClean.length > 22 ? "…" : ""} ❯`;
      nextBottom.style.visibility = "visible";
    } else {
      nextBottom.textContent = "🎉 Completed";
      nextBottom.style.visibility = "visible";
    }

    // Update Counters
    topNav.querySelector("#w3-counter").textContent = `Module ${index + 1} of ${modules.length}`;
    mobileBar.querySelector("#w3-mobile-badge").textContent = `${index + 1} / ${modules.length}`;

    // Update URL Hash and Title
    if (updateHash && location.hash !== `#${mod.id}`) {
      history.pushState(null, "", `#${mod.id}`);
    }
    setTitle(`${mod.headingClean} · ${currentTutorial.name} Material`);

    // Smooth scroll to top of reading area
    if (shouldScroll) {
      const topOffset = 115;
      const targetY = mainPane.getBoundingClientRect().top + window.pageYOffset - topOffset;
      window.scrollTo({ top: Math.max(0, targetY), behavior: "smooth" });
    }
  }

  // Handle Hash on load and hash change
  function syncFromHash(shouldScroll = false) {
    const rawHash = location.hash.replace(/^#/, "");
    // Check if hash points to a subtopic, e.g. "m1-sub-2"
    if (rawHash.includes("-sub-")) {
      const modId = rawHash.split("-sub-")[0];
      const mIdx = modules.findIndex((m) => m.id === modId);
      if (mIdx >= 0) {
        showModule(mIdx, false, false);
        const targetEl = document.getElementById(rawHash);
        if (targetEl) {
          const topOffset = 120;
          const targetY = targetEl.getBoundingClientRect().top + window.pageYOffset - topOffset;
          window.scrollTo({ top: Math.max(0, targetY), behavior: "smooth" });
        }
        return;
      }
    }
    const foundIdx = modules.findIndex((m) => m.id === rawHash);
    showModule(foundIdx >= 0 ? foundIdx : 0, false, shouldScroll);
  }

  window.addEventListener("hashchange", () => syncFromHash(true));
  syncFromHash(false);

  // Sidebar item click listeners (for module headings)
  sidebar.addEventListener("click", (e) => {
    const link = e.target.closest(".w3-sidebar-item");
    if (link) {
      e.preventDefault();
      const id = link.dataset.id;
      const idx = modules.findIndex((m) => m.id === id);
      if (idx >= 0) {
        showModule(idx, true, true);
        setDrawerOpen(false);
      }
      return;
    }

    // Subtopic click listener
    const subLink = e.target.closest(".w3-subtopic-link");
    if (subLink) {
      e.preventDefault();
      const subId = subLink.dataset.subId;
      const targetEl = document.getElementById(subId);
      if (targetEl) {
        const topOffset = 120;
        const targetY = targetEl.getBoundingClientRect().top + window.pageYOffset - topOffset;
        window.scrollTo({ top: Math.max(0, targetY), behavior: "smooth" });
        history.pushState(null, "", `#${subId}`);
      }
      setDrawerOpen(false);
    }
  });

  // Top Nav clicks
  topNav.querySelector("#w3-prev-top").addEventListener("click", () => showModule(currentIdx - 1, true, true));
  topNav.querySelector("#w3-next-top").addEventListener("click", () => showModule(currentIdx + 1, true, true));

  // Bottom Nav clicks
  bottomNav.querySelector("#w3-prev-bottom").addEventListener("click", () => showModule(currentIdx - 1, true, true));
  bottomNav.querySelector("#w3-next-bottom").addEventListener("click", () => {
    if (currentIdx < modules.length - 1) showModule(currentIdx + 1, true, true);
  });
  bottomNav.querySelector("#w3-top-link").addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Mobile bar clicks
  mobileBar.querySelector("#w3-m-prev").addEventListener("click", () => showModule(currentIdx - 1, true, true));
  mobileBar.querySelector("#w3-m-next").addEventListener("click", () => showModule(currentIdx + 1, true, true));
  mobileBar.querySelector("#w3-open-sidebar").addEventListener("click", () => setDrawerOpen(true));

  // Drawer close & overlay
  sidebar.querySelector("#w3-sidebar-close").addEventListener("click", () => setDrawerOpen(false));
  overlay.addEventListener("click", () => setDrawerOpen(false));

  // Filter search in sidebar
  const searchInput = sidebar.querySelector("#w3-module-search");
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();
    const groups = sidebar.querySelectorAll(".w3-heading-group");
    groups.forEach((group) => {
      const id = group.dataset.id;
      const mod = modules.find((m) => m.id === id);
      if (!mod) return;
      const hasSubMatch = mod.subtopics.some((st) => st.title.toLowerCase().includes(query));
      const match =
        !query ||
        mod.headingClean.toLowerCase().includes(query) ||
        mod.fullTitle.toLowerCase().includes(query) ||
        mod.sub.toLowerCase().includes(query) ||
        String(mod.index + 1) === query ||
        hasSubMatch;
      group.style.display = match ? "block" : "none";
    });
  });

  // Wide tables scroll sideways on small screens
  mainPane.querySelectorAll(".topic table").forEach((table) => {
    if (!table.parentElement.classList.contains("table-wrap")) {
      const wrap = document.createElement("div");
      wrap.className = "table-wrap";
      table.replaceWith(wrap);
      wrap.append(table);
    }
  });
});


