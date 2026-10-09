import { page, api, esc, media, getProfile, projectCard, postCard, setTitle } from "../ui.js";
import { educationList, jobsList } from "../parts.js";

page(async (app) => {
  const [profile, stats, projects, skills, posts, jobs, education] = await Promise.all([
    getProfile(), api("stats/"), api("projects/?is_featured=true&page_size=6"),
    api("skills/?is_featured=true"), api("blog/posts/?page_size=3"), api("experience/"), api("education/"),
  ]);
  const fullName = (profile.full_name && profile.full_name !== "Your Name") ? profile.full_name : "Naveenkumar";
  setTitle(fullName, profile.headline);
  const counts = [["Projects", stats.projects], ["Lessons", stats.study_materials], ["Topics", stats.study_categories],
    ["Skills", stats.skills], ["Certifications", stats.certifications]].filter(([, n]) => n > 0);
  const contact = [
    ["📍", esc(profile.location)],
    ["✉️", profile.email && `<a href="mailto:${esc(profile.email)}">${esc(profile.email)}</a>`],
    ["📞", profile.phone && `<a href="tel:${esc(profile.phone.replace(/\s/g, ""))}">${esc(profile.phone)}</a>`],
    ["💼", profile.linkedin_url && `<a href="${esc(profile.linkedin_url)}" target="_blank" rel="noopener">LinkedIn</a>`],
    ["💻", profile.github_url && `<a href="${esc(profile.github_url)}" target="_blank" rel="noopener">GitHub</a>`],
  ].filter(([, v]) => v);

  app.innerHTML = `
    <section class="hero">
      <canvas id="hero-canvas" aria-hidden="true"></canvas>
      <div class="wrap hero-inner">
        ${profile.photo ? `<img src="${esc(media(profile.photo))}" alt="${esc(fullName)}" class="avatar-lg">` : ""}
        <p class="eyebrow">${esc(profile.headline)}</p>
        <h1>Hi, I'm ${esc(fullName)}</h1>
        <p class="lead">${esc(profile.tagline)}</p>
        <div class="chips center">${profile.hero_badges_list.map((b) => `<span class="chip">${esc(b)}</span>`).join("")}</div>
        <div class="actions center">
          <a href="projects.html" class="btn">View projects</a>
          <a href="resume.html" class="btn btn-ghost">Resume</a>
          <a href="contact.html" class="btn btn-ghost">Contact me</a>
        </div>
      </div>
    </section>
    <section class="wrap stats">${counts.map(([label, n]) => `<div class="stat"><strong>${n}</strong><span>${label}</span></div>`).join("")}</section>
    ${profile.short_bio || contact.length ? `<section class="wrap section">
      <div class="grid two about-home">
        <div>
          <h2>About me</h2>
          ${profile.short_bio ? `<p class="lead">${esc(profile.short_bio)}</p>` : ""}
          ${profile.professional_goals ? `<p>${esc(profile.professional_goals)}</p>` : ""}
          <a href="about.html">More about me →</a>
        </div>
        ${contact.length ? `<div class="card contact-card">${contact.map(([icon, v]) => `<p><span aria-hidden="true">${icon}</span> ${v}</p>`).join("")}</div>` : ""}
      </div>
    </section>` : ""}
    ${projects.results.length ? `<section class="wrap section">
      <div class="section-head"><h2>Featured projects</h2><a href="projects.html">All projects →</a></div>
      <div class="grid">${projects.results.map(projectCard).join("")}</div></section>` : ""}
    ${skills.length ? `<section class="wrap section">
      <div class="section-head"><h2>Core skills</h2><a href="skills.html">All skills →</a></div>
      <div class="chips">${skills.map((s) => `<span class="chip chip-lg">${esc(s.name)}</span>`).join("")}</div></section>` : ""}
    ${jobs.length || education.length ? `<section class="wrap section">
      <div class="grid two">
        ${jobs.length ? `<div><div class="section-head"><h2>Experience</h2><a href="experience.html">Details →</a></div>${jobsList(jobs)}</div>` : ""}
        ${education.length ? `<div><div class="section-head"><h2>Education</h2><a href="resume.html">Resume →</a></div>${educationList(education)}</div>` : ""}
      </div>
    </section>` : ""}
    <section class="wrap section">
      <h2>Learn with me</h2>
      <div class="grid">
        <a class="card card-link" href="study.html"><h3>📘 Study materials</h3><p class="muted">Structured lessons from beginner to advanced.</p></a>
        <a class="card card-link" href="interview.html"><h3>💬 Interview prep</h3><p class="muted">Common questions with clear answers and code.</p></a>
        <a class="card card-link" href="practice.html"><h3>✅ Practice quizzes</h3><p class="muted">Test yourself with timed quizzes.</p></a>
      </div>
    </section>
    ${posts.results.length ? `<section class="wrap section">
      <div class="section-head"><h2>Latest posts</h2><a href="blog.html">Blog →</a></div>
      <div class="grid">${posts.results.map(postCard).join("")}</div></section>` : ""}`;

  heroAnimation(document.getElementById("hero-canvas"));
});

// Neural-network style particles behind the hero text.
function heroAnimation(canvas) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
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
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue("--network").trim();
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
