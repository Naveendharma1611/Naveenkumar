// Small progressive enhancements. Every page works without JavaScript.
(function () {
  const root = document.documentElement;

  // Theme toggle (remembered per browser)
  document.querySelector("[data-theme-toggle]")?.addEventListener("click", () => {
    const dark = root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
  });

  // Mobile menu
  document.querySelector("[data-toggle=nav]")?.addEventListener("click", () => {
    document.getElementById("nav").classList.toggle("open");
  });

  // Auto-submit filter selects, print button
  document.querySelectorAll("[data-autosubmit]").forEach((el) => el.addEventListener("change", () => el.form.submit()));
  document.querySelector("[data-print]")?.addEventListener("click", () => window.print());

  // Syntax highlighting + copy buttons on code blocks
  document.querySelectorAll("pre code").forEach((block) => {
    if (window.hljs) hljs.highlightElement(block);
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", () => {
      navigator.clipboard.writeText(block.innerText).then(() => {
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = "Copy"), 1500);
      });
    });
    block.parentElement.appendChild(btn);
  });

  // Quiz countdown: auto-submits when time runs out
  const quiz = document.getElementById("quiz-form");
  const timer = document.getElementById("timer");
  if (quiz && timer && quiz.dataset.minutes) {
    let left = Number(quiz.dataset.minutes) * 60;
    const tick = setInterval(() => {
      left -= 1;
      const m = Math.floor(left / 60), s = String(left % 60).padStart(2, "0");
      timer.textContent = `⏱ ${m}:${s}`;
      timer.classList.toggle("low", left <= 30);
      if (left <= 0) {
        clearInterval(tick);
        quiz.elements.timed_out.value = "1";
        quiz.submit();
      }
    }, 1000);
    quiz.addEventListener("submit", () => clearInterval(tick));
  }

  // Hero: animated neural-network style particles
  const canvas = document.getElementById("hero-canvas");
  if (canvas && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const ctx = canvas.getContext("2d");
    let w, h, nodes;
    const resize = () => {
      w = canvas.width = canvas.offsetWidth;
      h = canvas.height = canvas.offsetHeight;
      nodes = Array.from({ length: Math.min(70, Math.floor(w / 18)) }, () => ({
        x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
      }));
    };
    const draw = () => {
      const color = getComputedStyle(root).getPropertyValue("--network").trim();
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = ctx.strokeStyle = color;
      for (const n of nodes) {
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;
        ctx.beginPath(); ctx.arc(n.x, n.y, 2, 0, 7); ctx.fill();
      }
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const d = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
          if (d < 120) {
            ctx.globalAlpha = 1 - d / 120;
            ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(nodes[j].x, nodes[j].y); ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(draw);
    };
    resize();
    addEventListener("resize", resize);
    draw();
  }
})();
