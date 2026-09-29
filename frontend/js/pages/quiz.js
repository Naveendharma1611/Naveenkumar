import { page, api, auth, esc, md, param, enhance, toast, setTitle } from "../ui.js";

page(async (app) => {
  const slug = param("slug");
  const quiz = await api(`quizzes/${encodeURIComponent(slug)}/`);
  setTitle(quiz.title, quiz.description);
  const next = encodeURIComponent(`quiz.html?slug=${slug}`);
  const header = `<a href="practice.html" class="muted">← All quizzes</a><h1>${esc(quiz.title)}</h1>`;
  let timer;

  function intro() {
    app.innerHTML = `<section class="wrap section narrow">${header}
      ${quiz.description ? `<p class="lead">${esc(quiz.description)}</p>` : ""}
      <p>${quiz.question_count} questions · ${quiz.time_limit_minutes ? `${quiz.time_limit_minutes} minute limit` : "No time limit"} · ${esc(quiz.difficulty_label)}</p>
      ${auth.isStudent() ? "" : `<p class="muted">${auth.user ? 'Upgrade to a student account on your <a href="account.html">Account page</a>'
        : `<a href="login.html?next=${next}">Log in</a> as a student`} to save your score.</p>`}
      ${quiz.questions.length ? '<button class="btn" id="start">Start quiz</button>' : '<p class="muted">This quiz has no questions yet.</p>'}
      <div id="leaderboard"></div>
    </section>`;
    app.querySelector("#start")?.addEventListener("click", () => start().catch((err) => toast(err.message, "error")));
    if (quiz.show_leaderboard) leaderboard();
  }

  async function start() {
    let attemptId = null;
    if (auth.isStudent()) attemptId = (await api(`quizzes/${slug}/start/`, { method: "POST" })).attempt_id;
    app.innerHTML = `<section class="wrap section narrow">${header}
      <form id="quiz-form" class="stack">
        ${quiz.time_limit_minutes ? `<div class="timer" id="timer">⏱ ${quiz.time_limit_minutes}:00</div>` : ""}
        ${quiz.questions.map((q, i) => `
          <fieldset class="card">
            <legend class="badge">Q${i + 1} · ${esc(q.type_label)} · ${q.points} pt</legend>
            <div class="prose">${md(q.prompt)}</div>
            ${q.code ? `<pre><code class="language-${esc(q.code_language)}">${esc(q.code)}</code></pre>` : ""}
            ${q.type === "MCQ"
              ? q.options.map((o, j) => `<label class="option"><input type="radio" name="${q.id}" value="${j}"> ${esc(o)}</label>`).join("")
              : `<textarea name="${q.id}" rows="4" class="mono" placeholder="Your answer"></textarea>`}
          </fieldset>`).join("")}
        <button class="btn" type="submit">Submit answers</button>
      </form>
    </section>`;
    enhance(app);
    const form = app.querySelector("#quiz-form");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      clearInterval(timer);
      form.querySelector("[type=submit]").disabled = true;
      const answers = Object.fromEntries(new FormData(form));
      try {
        showResults(await api(`quizzes/${slug}/submit/`, { method: "POST", body: attemptId ? { attempt_id: attemptId, answers } : { answers } }), answers);
      } catch (err) {
        toast(err.message, "error");
        form.querySelector("[type=submit]").disabled = false;
      }
    });
    if (quiz.time_limit_minutes) startTimer(form, quiz.time_limit_minutes * 60);
  }

  function startTimer(form, seconds) {
    const el = app.querySelector("#timer");
    timer = setInterval(() => {
      seconds -= 1;
      el.textContent = `⏱ ${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
      el.classList.toggle("low", seconds <= 30);
      if (seconds <= 0) { clearInterval(timer); toast("Time's up! Submitting…", "error"); form.requestSubmit(); }
    }, 1000);
  }

  function showResults(res, answers) {
    const byId = Object.fromEntries(quiz.questions.map((q) => [q.id, q]));
    const answerText = (q, a) => (q.type === "MCQ" && a !== undefined ? q.options[Number(a)] : a) || "—";
    app.innerHTML = `<section class="wrap section narrow">${header}
      <div class="card score"><strong>${res.percent}%</strong><span>${res.score} / ${res.max_score} points</span>
        ${res.saved ? '<small class="muted">Saved to your dashboard.</small>' : ""}</div>
      ${res.results.map((r) => {
        const q = byId[r.question_id];
        const correct = q.type === "MCQ" ? q.options[r.correct_option] : r.accepted_answers.join(" / ");
        return `<div class="card result ${r.correct === true ? "ok" : r.correct === false ? "bad" : ""}">
          <div class="prose">${md(q.prompt)}</div>
          ${q.code ? `<pre><code class="language-${esc(q.code_language)}">${esc(q.code)}</code></pre>` : ""}
          <p>Your answer: <strong>${esc(answerText(q, answers[q.id]))}</strong>
            ${r.correct === true ? "✔ Correct" : r.correct === false ? `✘ Wrong${correct ? ` — correct: <strong>${esc(correct)}</strong>` : ""}` : "(self-review)"}</p>
          ${r.explanation ? `<div class="prose muted">${md(r.explanation)}</div>` : ""}
        </div>`;
      }).join("")}
      <button class="btn" id="again">Try again</button>
      <div id="leaderboard"></div>
    </section>`;
    enhance(app);
    app.querySelector("#again").addEventListener("click", intro);
    if (quiz.show_leaderboard) leaderboard();
    scrollTo(0, 0);
  }

  async function leaderboard() {
    const rows = await api(`quizzes/${slug}/leaderboard/`).catch(() => []);
    if (!rows.length) return;
    app.querySelector("#leaderboard").innerHTML = `<h2>Leaderboard</h2>
      <table class="table"><tr><th>#</th><th>Name</th><th>Best score</th></tr>
      ${rows.map((r) => `<tr><td>${r.rank}</td><td>${esc(r.name)}</td><td>${r.percent}%</td></tr>`).join("")}</table>`;
  }

  intro();
});
