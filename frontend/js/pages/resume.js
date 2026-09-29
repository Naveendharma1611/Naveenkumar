import { page, api, esc, media, setTitle } from "../ui.js";
import { educationList, jobsList } from "../parts.js";

page(async (app) => {
  setTitle("Resume");
  const r = await api("resume/");
  const p = r.profile;
  const contact = [p.email, p.phone, p.location, p.linkedin_url, p.github_url].filter(Boolean).map(esc).join(" · ");
  app.innerHTML = `<section class="wrap section narrow resume">
    <div class="actions no-print">
      <button class="btn" id="print">Print / Save as PDF</button>
      ${p.resume_pdf ? `<a class="btn btn-ghost" href="${esc(media(p.resume_pdf))}" download>Download PDF</a>` : ""}
    </div>
    <h1>${esc(p.full_name)}</h1>
    <p class="lead">${esc(p.headline)}</p>
    <p class="muted">${contact}</p>
    ${p.career_objective ? `<h2>Objective</h2><p>${esc(p.career_objective)}</p>` : ""}
    <h2>Experience</h2>${jobsList(r.experience)}
    ${r.education.length ? `<h2>Education</h2>${educationList(r.education)}` : ""}
    ${r.skills.length ? `<h2>Skills</h2>${r.skills.map((g) => `<p><strong>${esc(g.category)}:</strong> ${g.skills.map(esc).join(", ")}</p>`).join("")}` : ""}
    ${r.projects.length ? `<h2>Projects</h2><ul>${r.projects.map((x) => `<li><a href="project.html?slug=${esc(x.slug)}">${esc(x.title)}</a> — ${esc(x.summary)}</li>`).join("")}</ul>` : ""}
    ${r.certificates.length ? `<h2>Certifications</h2><ul>${r.certificates.map((c) => `<li>${esc(c.name)} — ${esc(c.provider)} (${esc(String(c.issue_date).slice(0, 4))})</li>`).join("")}</ul>` : ""}
    ${r.achievements.length ? `<h2>Achievements</h2><ul>${r.achievements.map((a) => `<li>${esc(a.title)}</li>`).join("")}</ul>` : ""}
  </section>`;
  app.querySelector("#print").addEventListener("click", () => window.print());
});
