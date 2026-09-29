import { page, api, auth, esc, fmtDate, toast, requireLogin, setTitle, API_ORIGIN } from "../ui.js";

const TABS = [["overview", "Overview"], ["users", "Users"], ["messages", "Messages"]];

page(async (app) => {
  requireLogin({ admin: true });
  setTitle("Admin");
  app.innerHTML = `<section class="wrap section">
    <div class="section-head"><h1>Admin dashboard</h1>
      <a class="btn" href="${API_ORIGIN}/django-admin/" target="_blank" rel="noopener">Edit content in Django admin ↗</a></div>
    <nav class="tabs">${TABS.map(([id, label]) => `<a href="#${id}" data-tab="${id}">${label}</a>`).join("")}</nav>
    <div id="panel"></div>
  </section>`;
  const panel = app.querySelector("#panel");
  const show = async () => {
    const tab = TABS.some(([id]) => `#${id}` === location.hash) ? location.hash.slice(1) : "overview";
    app.querySelectorAll("[data-tab]").forEach((a) => a.classList.toggle("active", a.dataset.tab === tab));
    panel.innerHTML = '<p class="muted">Loading…</p>';
    try {
      await { overview, users, messages }[tab](panel);
    } catch (err) {
      panel.innerHTML = `<div class="alert error">${esc(err.message)}</div>`;
    }
  };
  addEventListener("hashchange", show);
  await show();
});

async function overview(panel) {
  const o = await api("admin/overview/");
  const pair = (x) => `${x.published}<small class="muted"> / ${x.total}</small>`;
  const cards = [
    ["Users", `${o.users.total}`, `${o.users.students} students · ${o.users.visitors} visitors`],
    ["Projects", pair(o.projects), "published / total"], ["Lessons", pair(o.lessons), `${o.courses.published} courses`],
    ["Topics", pair(o.study_categories), "published / total"], ["Interview questions", pair(o.interview_questions), "published / total"],
    ["Quizzes", pair(o.quizzes), `${o.quiz_attempts} attempts`], ["Certificates", pair(o.certificates), "published / total"],
    ["Blog posts", pair(o.blog_posts), "published / total"], ["Unread messages", `${o.unread_messages}`, '<a href="#messages">Open inbox</a>'],
  ];
  panel.innerHTML = `
    <div class="stats">${cards.map(([label, value, note]) => `<div class="stat"><strong>${value}</strong><span>${label}</span><br><small class="muted">${note}</small></div>`).join("")}</div>
    <h2>Newest users</h2>
    <div class="table-wrap"><table class="table"><tr><th>Name</th><th>Email</th><th>Role</th><th>Joined</th></tr>
      ${o.recent_users.map((u) => `<tr><td>${esc(u.full_name)}</td><td>${esc(u.email)}</td><td>${esc(u.role)}</td><td>${fmtDate(u.date_joined)}</td></tr>`).join("")}
    </table></div>`;
}

async function users(panel, search = "", role = "") {
  const qs = new URLSearchParams({ page_size: 100 });
  if (search) qs.set("search", search);
  if (role) qs.set("role", role);
  const data = await api(`admin/users/?${qs}`);
  const roles = ["STUDENT", "VISITOR", "ADMIN"];
  panel.innerHTML = `
    <form class="filters" id="user-filter">
      <input name="search" value="${esc(search)}" placeholder="Search name or email" aria-label="Search users">
      <select name="role" aria-label="Role"><option value="">All roles</option>${roles.map((r) => `<option ${r === role ? "selected" : ""}>${r}</option>`).join("")}</select>
      <button class="btn">Filter</button>
    </form>
    <p class="muted">${data.count} user(s)</p>
    <div class="table-wrap"><table class="table"><tr><th>Name</th><th>Email</th><th>Role</th><th>Active</th><th>Last login</th><th></th></tr>
      ${data.results.map((u) => `<tr data-id="${u.id}">
        <td>${esc(u.full_name)}</td><td>${esc(u.email)}</td>
        <td><select data-field="role" aria-label="Role" ${u.id === auth.user.id ? "disabled" : ""}>${roles.map((r) => `<option ${r === u.role ? "selected" : ""}>${r}</option>`).join("")}</select></td>
        <td><input type="checkbox" data-field="is_active" aria-label="Active" ${u.is_active ? "checked" : ""} ${u.id === auth.user.id ? "disabled" : ""}></td>
        <td>${u.last_login ? fmtDate(u.last_login) : "—"}</td>
        <td>${u.id === auth.user.id ? "" : '<button class="link danger" data-delete>Delete</button>'}</td>
      </tr>`).join("")}
    </table></div>`;

  panel.querySelector("#user-filter").addEventListener("submit", (e) => {
    e.preventDefault();
    users(panel, e.target.search.value.trim(), e.target.role.value);
  });
  panel.querySelectorAll("[data-field]").forEach((input) => input.addEventListener("change", async () => {
    const id = input.closest("tr").dataset.id;
    const value = input.type === "checkbox" ? input.checked : input.value;
    try {
      await api(`admin/users/${id}/`, { method: "PATCH", body: { [input.dataset.field]: value } });
      toast("User updated");
    } catch (err) { toast(err.message, "error"); }
  }));
  panel.querySelectorAll("[data-delete]").forEach((btn) => btn.addEventListener("click", async () => {
    const row = btn.closest("tr");
    if (!confirm(`Delete ${row.children[1].textContent}? This cannot be undone.`)) return;
    try {
      await api(`admin/users/${row.dataset.id}/`, { method: "DELETE" });
      row.remove();
      toast("User deleted");
    } catch (err) { toast(err.message, "error"); }
  }));
}

async function messages(panel, unreadOnly = false) {
  const data = await api(`admin/messages/?page_size=100${unreadOnly ? "&is_read=false" : ""}`);
  panel.innerHTML = `
    <label class="option inline-option"><input type="checkbox" id="unread" ${unreadOnly ? "checked" : ""}> Unread only</label>
    ${data.results.map((m) => `<div class="card message ${m.is_read ? "" : "unread"}" data-id="${m.id}">
      <div class="section-head"><strong>${esc(m.subject)}</strong><small class="muted">${fmtDate(m.created_at)}</small></div>
      <p class="muted">${esc(m.name)} · <a href="mailto:${esc(m.email)}?subject=${encodeURIComponent(`Re: ${m.subject}`)}">${esc(m.email)}</a></p>
      <p class="pre-line">${esc(m.message)}</p>
      <div class="actions">
        <button class="btn btn-ghost" data-read="${m.is_read ? "false" : "true"}">${m.is_read ? "Mark unread" : "Mark read"}</button>
        <button class="btn btn-ghost danger" data-delete>Delete</button>
      </div>
    </div>`).join("") || '<p class="muted">No messages.</p>'}`;

  panel.querySelector("#unread").addEventListener("change", (e) => messages(panel, e.target.checked));
  panel.querySelectorAll(".message").forEach((card) => card.addEventListener("click", async (e) => {
    const id = card.dataset.id;
    try {
      if (e.target.matches("[data-read]")) {
        await api(`admin/messages/${id}/`, { method: "PATCH", body: { is_read: e.target.dataset.read === "true" } });
        await messages(panel, unreadOnly);
      } else if (e.target.matches("[data-delete]") && confirm("Delete this message?")) {
        await api(`admin/messages/${id}/`, { method: "DELETE" });
        card.remove();
        toast("Message deleted");
      }
    } catch (err) { toast(err.message, "error"); }
  }));
}
