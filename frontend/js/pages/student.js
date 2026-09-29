import { page, api, esc, route, fmtDate, empty, requireLogin, setTitle } from "../ui.js";

page(async (app) => {
  requireLogin({ student: true });
  setTitle("Dashboard");
  const [d, bookmarks, attempts] = await Promise.all([
    api("student/dashboard/"), api("study/bookmarks/"), api("student/quiz-attempts/?page_size=20"),
  ]);
  const stats = [["Lessons completed", d.lessons_completed], ["Courses completed", d.courses_completed],
    ["Quiz attempts", d.quiz_attempts], ["Average quiz score", d.average_quiz_score == null ? "—" : `${Math.round(d.average_quiz_score)}%`],
    ["Bookmarks", d.bookmarks]];

  app.innerHTML = `<section class="wrap section">
    <h1>Welcome back, ${esc(d.name)} 👋</h1>
    <div class="stats">${stats.map(([l, n]) => `<div class="stat"><strong>${n}</strong><span>${l}</span></div>`).join("")}</div>
    <div class="grid two">
      <div class="card"><h2>Progress</h2>
        ${d.category_progress.filter((p) => p.total).map((p) => `
          <p><a href="category.html?c=${esc(p.slug)}">${esc(p.name)}</a> <small class="muted">${p.completed}/${p.total}</small></p>
          <div class="bar"><span style="width:${p.percent}%"></span></div>`).join("") || '<p class="muted">Start a <a href="study.html">lesson</a> to see progress.</p>'}
      </div>
      <div class="card"><h2>Recent activity</h2>
        <ul>${d.recent_activity.map((a) => `<li><a href="${esc(route(a.link))}">${esc(a.title)}</a> <small class="muted">${fmtDate(a.at)}</small></li>`).join("")
          || '<li class="muted">Nothing yet.</li>'}</ul>
      </div>
      <div class="card"><h2>Bookmarks</h2>
        <ul>${bookmarks.map((b) => `<li><a href="lesson.html?c=${esc(b.category_slug)}&l=${esc(b.slug)}">${esc(b.title)}</a> <small class="muted">${esc(b.category_name)}</small></li>`).join("")
          || '<li class="muted">No bookmarks yet.</li>'}</ul>
      </div>
      <div class="card"><h2>Quiz attempts</h2>
        ${attempts.results.length ? `<table class="table"><tr><th>Quiz</th><th>Score</th><th>Date</th></tr>
          ${attempts.results.map((a) => `<tr><td><a href="quiz.html?slug=${esc(a.quiz_slug)}">${esc(a.quiz_title)}</a></td>
            <td>${a.percent}%</td><td>${fmtDate(a.submitted_at)}</td></tr>`).join("")}</table>`
          : empty("No attempts yet.") + '<a class="btn btn-ghost" href="practice.html">Take a quiz</a>'}
      </div>
    </div>
  </section>`;
});
