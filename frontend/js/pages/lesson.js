import { page, api, auth, esc, md, param, videoEmbed, toast, onSubmit, setTitle } from "../ui.js";
import { materialItem } from "../parts.js";

page(async (app) => {
  const c = param("c"), l = param("l");
  const lesson = await api(`study/lesson/${encodeURIComponent(c)}/${encodeURIComponent(l)}/`);
  setTitle(lesson.title, lesson.summary);
  const href = (slug) => `lesson.html?c=${encodeURIComponent(c)}&l=${encodeURIComponent(slug)}`;

  app.innerHTML = `<section class="wrap section with-sidebar">
    <aside class="sidebar card">
      <a href="category.html?c=${esc(c)}" class="muted">← ${esc(lesson.category_name)}</a>
      <h3>${esc(lesson.course_title)}</h3>
      <ol class="lessons">${lesson.course_lessons.map((x) => `
        <li><a href="${href(x.slug)}" ${x.slug === lesson.slug ? 'class="active"' : ""}>${esc(x.title)}</a></li>`).join("")}</ol>
    </aside>
    <article>
      <p><span class="badge">${esc(lesson.course_level)}</span>${lesson.estimated_minutes ? ` <small class="muted">${lesson.estimated_minutes} min</small>` : ""}</p>
      <h1>${esc(lesson.title)}</h1>
      ${lesson.summary ? `<p class="lead">${esc(lesson.summary)}</p>` : ""}
      <div class="actions" id="lesson-actions"></div>
      ${lesson.video_url ? videoEmbed(lesson.video_url) : ""}
      <div class="prose">${md(lesson.content)}</div>
      ${lesson.materials.length ? `<h2>Materials</h2>${lesson.materials.map(materialItem).join("")}` : ""}
      <div id="notes"></div>
      <nav class="pager">
        ${lesson.previous ? `<a class="btn btn-ghost" href="${href(lesson.previous.slug)}">← ${esc(lesson.previous.title)}</a>` : "<span></span>"}
        ${lesson.next ? `<a class="btn" href="${href(lesson.next.slug)}">${esc(lesson.next.title)} →</a>` : ""}
      </nav>
    </article>
  </section>`;

  const actions = app.querySelector("#lesson-actions");
  const state = lesson.user_state;
  if (!auth.user || !state) {
    const next = encodeURIComponent(href(lesson.slug));
    actions.innerHTML = `<p class="muted"><a href="login.html?next=${next}">Log in</a> to track progress, bookmark and take notes.</p>`;
    return;
  }
  if (!auth.isStudent()) {
    actions.innerHTML = '<p class="muted">Upgrade to a student account on your <a href="account.html">Account page</a> to track progress.</p>';
    return;
  }

  const drawActions = () => {
    actions.innerHTML = `
      <button class="btn ${state.completed ? "" : "btn-ghost"}" data-act="complete">${state.completed ? "✔ Completed" : "Mark as complete"}</button>
      <button class="btn btn-ghost" data-act="bookmark">${state.bookmarked ? "★ Bookmarked" : "☆ Bookmark"}</button>`;
  };
  drawActions();
  actions.addEventListener("click", async (e) => {
    const act = e.target.closest("[data-act]")?.dataset.act;
    if (!act) return;
    try {
      if (act === "complete") {
        const res = await api("study/progress/", { method: "POST", body: { lesson: lesson.id, completed: !state.completed } });
        state.completed = res.completed;
        toast(state.completed ? "Lesson completed 🎉" : "Marked as not completed");
      } else {
        state.bookmarked = (await api("study/bookmarks/", { method: "POST", body: { lesson: lesson.id } })).bookmarked;
      }
      drawActions();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  const notes = app.querySelector("#notes");
  notes.innerHTML = `<h2>My notes</h2>
    <form class="stack"><textarea name="content" rows="6" placeholder="Write your notes for this lesson…">${esc(state.note)}</textarea>
    <button class="btn" type="submit">Save note</button></form>`;
  onSubmit(notes.querySelector("form"), async ({ content }) => {
    await api("study/notes/", { method: "PUT", body: { lesson: lesson.id, content } });
    toast("Note saved");
  });
});
