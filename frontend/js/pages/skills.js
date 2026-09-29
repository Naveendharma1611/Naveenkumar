import { page, api, esc, empty, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Skills");
  const skills = await api("skills/");
  const groups = new Map();
  for (const s of skills) {
    if (!groups.has(s.category_label)) groups.set(s.category_label, []);
    groups.get(s.category_label).push(s);
  }
  app.innerHTML = `<section class="wrap section"><h1>Skills</h1>
    ${[...groups].map(([label, items]) => `<h2>${esc(label)}</h2><div class="grid">${items.map((s) => `
      <div class="card">
        <h3>${esc(s.name)} ${s.proficiency_label ? `<small class="badge">${esc(s.proficiency_label)}</small>` : ""}</h3>
        ${s.description ? `<p class="muted">${esc(s.description)}</p>` : ""}
        ${s.proficiency_percent ? `<div class="bar"><span style="width:${Number(s.proficiency_percent)}%"></span></div>` : ""}
      </div>`).join("")}</div>`).join("") || empty("No skills added yet.")}
  </section>`;
});
