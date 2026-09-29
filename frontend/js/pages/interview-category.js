import { page, api, esc, md, param, pager, empty, setTitle } from "../ui.js";

const LEVELS = [["", "All"], ["EASY", "Easy"], ["MEDIUM", "Medium"], ["HARD", "Hard"]];

page(async (app) => {
  const c = param("c"), difficulty = param("difficulty"), pageNo = Number(param("page")) || 1, size = 50;
  const qs = new URLSearchParams({ category__slug: c, page: pageNo, page_size: size });
  if (difficulty) qs.set("difficulty", difficulty);
  const data = await api(`interview/questions/?${qs}`);
  const name = data.results[0]?.category_name || c;
  setTitle(`${name} interview questions`);

  app.innerHTML = `<section class="wrap section narrow">
    <a href="interview.html" class="muted">← All topics</a>
    <h1>${esc(name)} interview questions</h1>
    <div class="chips">${LEVELS.map(([v, l]) => `<a class="chip ${v === difficulty ? "on" : ""}" href="?c=${esc(c)}${v ? `&difficulty=${v}` : ""}">${l}</a>`).join("")}</div>
    <input id="filter" placeholder="Filter questions…" aria-label="Filter questions">
    <div id="questions">${data.results.map((q, i) => `
      <details class="card qa" id="q${q.id}">
        <summary><span class="badge">${esc(q.difficulty_label)}</span> ${(pageNo - 1) * size + i + 1}. ${esc(q.question)}</summary>
        <p><strong>Answer:</strong> ${esc(q.short_answer)}</p>
        ${q.detailed_answer ? `<div class="prose">${md(q.detailed_answer)}</div>` : ""}
        ${q.code ? `<pre><code class="language-${esc(q.code_language)}">${esc(q.code)}</code></pre>` : ""}
        ${q.example ? `<div class="prose">${md(q.example)}</div>` : ""}
        ${q.interview_tip ? `<div class="alert info">💡 ${esc(q.interview_tip)}</div>` : ""}
      </details>`).join("") || empty("No questions found.")}</div>
    ${pager(data, pageNo, size)}
  </section>`;

  app.querySelector("#filter").addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    app.querySelectorAll(".qa").forEach((el) => { el.hidden = !el.textContent.toLowerCase().includes(term); });
  });
  const target = location.hash && document.querySelector(location.hash);
  if (target) { target.open = true; target.scrollIntoView(); }
});
