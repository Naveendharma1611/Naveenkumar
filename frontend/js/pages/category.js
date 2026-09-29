import { page, api, auth, esc, param, empty, setTitle } from "../ui.js";
import { NOTES, materialItem, notesCard } from "../parts.js";

page(async (app) => {
  const slug = param("c");
  const c = await api(`study/categories/${encodeURIComponent(slug)}/`);
  setTitle(c.name, c.description);
  let progress = null;
  if (auth.isStudent()) {
    const d = await api("student/dashboard/").catch(() => null);
    progress = d?.category_progress.find((x) => x.slug === c.slug);
  }
  app.innerHTML = `<section class="wrap section narrow">
    <a href="study.html" class="muted">← All topics</a>
    <h1>${esc(c.name)}</h1>
    ${c.description ? `<p class="lead">${esc(c.description)}</p>` : ""}
    ${progress ? `<p class="muted">You have completed ${progress.completed} of ${progress.total} lessons.</p>
      <div class="bar"><span style="width:${progress.percent}%"></span></div>` : ""}
    ${NOTES[c.slug] ? notesCard(NOTES[c.slug]) : ""}
    ${c.courses.map((course) => `
      <div class="card" id="${esc(course.slug)}">
        <h2>${esc(course.title)} <span class="badge">${esc(course.level_label)}</span></h2>
        ${course.description ? `<p class="muted">${esc(course.description)}</p>` : ""}
        <ol class="lessons">${course.lessons.map((l) => `
          <li><a href="lesson.html?c=${esc(c.slug)}&l=${esc(l.slug)}">${esc(l.title)}</a>
          ${l.estimated_minutes ? `<small class="muted">${l.estimated_minutes} min</small>` : ""}</li>`).join("") || '<li class="muted">Lessons coming soon.</li>'}</ol>
        ${course.materials.map(materialItem).join("")}
      </div>`).join("") || (NOTES[c.slug] ? "" : empty("No courses yet."))}
  </section>`;
  if (location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
});
