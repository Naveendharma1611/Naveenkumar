import { page, api, esc, empty, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Practice quizzes");
  const data = await api("quizzes/?page_size=100");
  app.innerHTML = `<section class="wrap section">
    <h1>Practice quizzes</h1>
    <div class="grid">${data.results.map((q) => `
      <a class="card card-link" href="quiz.html?slug=${esc(q.slug)}">
        <span class="badge">${esc(q.difficulty_label)}</span>
        <h3>${esc(q.title)}</h3>
        ${q.description ? `<p class="muted">${esc(q.description.slice(0, 140))}</p>` : ""}
        <small class="muted">${q.question_count} questions${q.time_limit_minutes ? ` · ${q.time_limit_minutes} min` : ""}${q.category_name ? ` · ${esc(q.category_name)}` : ""}</small>
      </a>`).join("") || empty("No quizzes yet. Check back soon!")}</div>
  </section>`;
});
