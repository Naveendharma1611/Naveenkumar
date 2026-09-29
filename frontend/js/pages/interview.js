import { page, api, esc, plural, empty, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Interview preparation");
  const categories = await api("interview/categories/");
  app.innerHTML = `<section class="wrap section">
    <h1>Interview preparation</h1>
    <p class="lead">Real interview questions with short answers, detailed explanations, code and tips.</p>
    <div class="grid">${categories.map((c) => `
      <a class="card card-link" href="interview-category.html?c=${esc(c.slug)}">
        <h3>${esc(c.name)}</h3><small class="muted">${plural(c.question_count, "question")}</small>
      </a>`).join("") || empty("No questions yet.")}</div>
  </section>`;
});
