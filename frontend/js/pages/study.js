import { page, api, esc, plural, empty, setTitle } from "../ui.js";
import { NOTES, notesCard } from "../parts.js";

page(async (app) => {
  setTitle("Study materials");
  const categories = await api("study/categories/");
  const bySlug = Object.fromEntries(categories.map((c) => [c.slug, c]));
  const lessons = (c) => `${plural(c.course_count, "course")} · ${plural(c.lesson_count, "lesson")}`;

  // Subjects with complete notes get one large card; if the backend also has lessons for
  // that subject, the card links to them instead of showing a second, smaller card.
  const lessonsLink = (slug) => {
    const c = bySlug[slug];
    return c?.lesson_count
      ? `<a class="card-extra" href="category.html?c=${esc(slug)}">📘 ${lessons(c)} with progress tracking →</a>` : "";
  };
  const topics = categories.filter((c) => !NOTES[c.slug]);

  app.innerHTML = `<section class="wrap section">
    <h1>Study materials</h1>
    <p class="lead">Pick a topic and learn step by step, from beginner to advanced.</p>
    <div class="grid notes-grid">${Object.entries(NOTES).map(([slug, n]) => notesCard(n, lessonsLink(slug))).join("")}</div>
    ${topics.length ? `<h2 class="topics-title">More topics</h2>
    <div class="grid">${topics.map((c) => `
      <a class="card card-link" href="category.html?c=${esc(c.slug)}">
        <h3>${esc(c.name)}</h3>
        ${c.description ? `<p class="muted">${esc(c.description.slice(0, 140))}</p>` : ""}
        <small class="muted">${c.lesson_count ? lessons(c) : "Coming soon"}</small>
      </a>`).join("")}</div>` : ""}
    ${!categories.length && !Object.keys(NOTES).length ? empty("No study materials yet.") : ""}
  </section>`;
});
