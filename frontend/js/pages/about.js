import { page, api, esc, md, media, getProfile, setTitle } from "../ui.js";
import { educationList } from "../parts.js";

page(async (app) => {
  setTitle("About");
  const [p, education, achievements] = await Promise.all([getProfile(), api("education/"), api("achievements/")]);
  const list = (title, items) => (items.length
    ? `<div class="card"><h3>${title}</h3><ul>${items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul></div>` : "");
  app.innerHTML = `<section class="wrap section narrow">
    ${p.photo ? `<img src="${esc(media(p.photo))}" alt="${esc(p.full_name)}" class="avatar-lg">` : ""}
    <h1>About me</h1>
    ${p.short_bio ? `<p class="lead">${esc(p.short_bio)}</p>` : ""}
    <div class="prose">${md(p.about)}</div>
    ${p.career_objective ? `<h2>Career objective</h2><p>${esc(p.career_objective)}</p>` : ""}
    ${p.professional_goals ? `<h2>Professional goals</h2><p>${esc(p.professional_goals)}</p>` : ""}
    <div class="grid two">${list("Technical interests", p.technical_interests_list)}${list("Currently learning", p.current_learning_list)}</div>
    ${education.length ? `<h2>Education</h2>${educationList(education)}` : ""}
    ${achievements.length ? `<h2>Achievements</h2><ul class="timeline">${achievements.map((a) => `
      <li><strong>${esc(a.title)}</strong>${a.date ? ` <small class="muted">${esc(a.date.slice(0, 7))}</small>` : ""}
      <p class="muted">${esc(a.description)}</p></li>`).join("")}</ul>` : ""}
  </section>`;
});
