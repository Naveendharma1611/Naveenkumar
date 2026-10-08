// Shared layout (header/footer), formatting helpers, cards and form handling.
import { api, auth, ApiError, API_ORIGIN } from "./api.js";

export { api, auth, ApiError, API_ORIGIN };

// ---------- Helpers ----------

export function esc(value) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  return String(value ?? "").replace(/[&<>"']/g, (c) => map[c]);
}
export const md = (text) => window.DOMPurify.sanitize(window.marked.parse(text || ""));
export const param = (name) => new URLSearchParams(location.search).get(name) || "";
export const split = (text, sep = ",") => (text || "").split(sep).map((s) => s.trim()).filter(Boolean);
export const media = (url) => (url && url.startsWith("/") ? API_ORIGIN + url : url);
export const fmtDate = (d, opts = { year: "numeric", month: "short", day: "numeric" }) =>
  d ? new Date(d).toLocaleDateString(undefined, opts) : "";
export const monthYear = (d) => fmtDate(d, { year: "numeric", month: "short" });
export const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

let profilePromise;
export const getProfile = () => (profilePromise ??= api("profile/"));

// Paths returned by the API (search results, dashboard activity) -> pages in this folder.
const ROUTES = [
  [/^\/projects\/([^/?#]+)/, (m) => `project.html?slug=${m[1]}`],
  [/^\/study-materials\/([^/?#]+)\/([^/?#]+)/, (m) => `lesson.html?c=${m[1]}&l=${m[2]}`],
  [/^\/study-materials\/([^/?#]+)(?:#(.+))?/, (m) => `category.html?c=${m[1]}${m[2] ? `#${m[2]}` : ""}`],
  [/^\/interview\/([^/?#]+)(?:\?q=(\d+))?/, (m) => `interview-category.html?c=${m[1]}${m[2] ? `#q${m[2]}` : ""}`],
  [/^\/blog\/([^/?#]+)/, (m) => `post.html?slug=${m[1]}`],
  [/^\/certificate\/([^/?#]+)/, (m) => `certificate.html?id=${m[1]}`],
  [/^\/practice\/([^/?#]+)/, (m) => `quiz.html?slug=${m[1]}`],
];
export function route(path) {
  for (const [re, to] of ROUTES) {
    const m = path.match(re);
    if (m) return to(m);
  }
  return path;
}

// Only allow redirects to pages in this site (prevents open redirects).
export function nextPage(fallback) {
  const next = param("next");
  return /^[\w-]+\.html(\?[^#]*)?(#.*)?$/.test(next) ? next : fallback;
}
export const homeFor = (user) => (user?.is_admin ? "admin.html" : user?.role === "STUDENT" ? "student.html" : "index.html");

// ---------- Layout ----------

const NAV = [
  ["about.html", "About"], ["projects.html", "Projects"], ["study.html", "Learn"], ["interview.html", "Interview"],
  ["practice.html", "Practice"], ["practice/", "Python Lab"], ["blog.html", "Blog"], ["contact.html", "Contact"],
];
const current = () => {
  const path = location.pathname.split("/").pop();
  return path || (location.pathname.startsWith("/practice/") ? "practice/" : "index.html");
};

function renderLayout() {
  const user = auth.user;
  const here = current();
  const header = document.createElement("header");
  header.className = "nav";
  header.innerHTML = `
    <div class="wrap nav-inner">
      <a href="index.html" class="brand" data-brand>Portfolio</a>
      <button class="icon-btn menu-btn" aria-label="Menu" aria-expanded="false">☰</button>
      <nav id="nav">
        ${NAV.map(([href, label]) => `<a href="${href}" ${here === href ? 'class="active"' : ""}>${label}</a>`).join("")}
        <form action="search.html" class="nav-search"><input name="q" placeholder="Search…" aria-label="Search"></form>
        ${user ? `
          ${user.is_admin ? '<a href="admin.html">Admin</a>' : ""}
          ${auth.isStudent() ? '<a href="student.html">Dashboard</a>' : ""}
          <a href="account.html">Account</a>
          <button class="link" data-logout>Log out</button>`
        : '<a href="login.html" class="btn btn-sm">Log in</a>'}
        <button class="icon-btn" data-theme-toggle aria-label="Toggle theme">◐</button>
      </nav>
    </div>`;
  document.body.prepend(header);

  const footer = document.createElement("footer");
  footer.className = "footer";
  footer.innerHTML = `
    <div class="wrap footer-inner">
      <p>© ${new Date().getFullYear()} <span data-brand>Portfolio</span>. Built with HTML, CSS &amp; JavaScript + Django.</p>
      <p data-social><a href="skills.html">Skills</a><a href="experience.html">Experience</a>
        <a href="certifications.html">Certifications</a><a href="resume.html">Resume</a></p>
    </div>`;
  document.body.append(footer);

  header.querySelector(".menu-btn").addEventListener("click", (e) => {
    const open = document.getElementById("nav").classList.toggle("open");
    e.currentTarget.setAttribute("aria-expanded", open);
  });
  header.querySelector("[data-theme-toggle]").addEventListener("click", () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch { /* ignore */ }
  });
  header.querySelector("[data-logout]")?.addEventListener("click", async () => {
    await api("auth/logout/", { method: "POST", body: { refresh: auth.refresh } }).catch(() => {});
    auth.clear();
    location.href = "index.html";
  });

  getProfile().then((p) => {
    document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = p.full_name));
    const social = footer.querySelector("[data-social]");
    if (p.github_url) social.insertAdjacentHTML("afterbegin", `<a href="${esc(p.github_url)}" target="_blank" rel="noopener">GitHub</a>`);
    if (p.linkedin_url) social.insertAdjacentHTML("afterbegin", `<a href="${esc(p.linkedin_url)}" target="_blank" rel="noopener">LinkedIn</a>`);
  }).catch(() => {});
}

export function setTitle(title, description) {
  document.title = title ? `${title} · Portfolio` : "Portfolio";
  if (description) document.querySelector('meta[name="description"]')?.setAttribute("content", description);
}

class Redirecting extends Error {}

/** Runs a page: draws the layout, then `render(app)`, and shows a friendly error if anything fails. */
export async function page(render) {
  renderLayout();
  const app = document.getElementById("app");
  try {
    await render(app);
    enhance(app);
  } catch (err) {
    if (err instanceof Redirecting) return;
    console.error(err);
    const notFound = err.status === 404;
    app.innerHTML = `<section class="wrap section auth"><div class="card">
      <h1>${notFound ? "Not found" : err.status === 403 ? "Access denied" : "Something went wrong"}</h1>
      <p>${esc(notFound ? "This page doesn't exist or isn't published yet." : err.message)}</p>
      <a class="btn" href="index.html">Go home</a></div></section>`;
  }
}

/** Sends visitors to the login page, or throws 403 when the role is wrong. */
export function requireLogin({ student = false, admin = false } = {}) {
  if (!auth.user) {
    location.replace(`login.html?next=${encodeURIComponent(current() + location.search)}`);
    throw new Redirecting();
  }
  if (admin && !auth.isAdmin()) throw new ApiError(403, { detail: "This page is for admins only." });
  if (student && !auth.isStudent()) {
    throw new ApiError(403, { detail: "This page is for student accounts. You can upgrade on your Account page." });
  }
}

/** Syntax highlighting and copy buttons for code blocks inside `root`. */
export function enhance(root) {
  root.querySelectorAll("pre code:not([data-done])").forEach((block) => {
    block.dataset.done = "1";
    if (window.hljs) window.hljs.highlightElement(block);
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", () => navigator.clipboard.writeText(block.innerText).then(() => {
      btn.textContent = "Copied!";
      setTimeout(() => (btn.textContent = "Copy"), 1500);
    }));
    block.parentElement.append(btn);
  });
}

export function toast(message, type = "success") {
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = message;
  document.body.append(el);
  setTimeout(() => el.remove(), 3000);
}

// ---------- Reusable markup ----------

export const chips = (items) => (items?.length ? `<div class="chips">${items.map((t) => `<span class="chip">${esc(t)}</span>`).join("")}</div>` : "");
export const empty = (text) => `<p class="muted">${esc(text)}</p>`;

export const projectCard = (p) => `
  <a class="card card-link" href="project.html?slug=${esc(p.slug)}">
    ${p.cover_image ? `<img src="${esc(p.cover_image)}" alt="" class="cover" loading="lazy">` : ""}
    <span class="badge">${esc(p.category_label)}</span>
    <h3>${esc(p.title)}</h3>
    <p class="muted">${esc(p.summary)}</p>
    ${chips(p.technologies.map((t) => t.name))}
  </a>`;

export const postCard = (p) => `
  <a class="card card-link" href="post.html?slug=${esc(p.slug)}">
    ${p.featured_image ? `<img src="${esc(p.featured_image)}" alt="" class="cover" loading="lazy">` : ""}
    ${p.category ? `<span class="badge">${esc(p.category.name)}</span>` : ""}
    <h3>${esc(p.title)}</h3>
    <p class="muted">${esc(p.excerpt)}</p>
    <small class="muted">${fmtDate(p.published_at)} · ${p.reading_minutes} min read</small>
  </a>`;

export function pager(data, page, size) {
  if (!data.next && !data.previous) return "";
  const url = (n) => { const q = new URLSearchParams(location.search); q.set("page", n); return `?${q}`; };
  return `<nav class="pagination">
    ${data.previous ? `<a class="btn btn-ghost" href="${url(page - 1)}">← Prev</a>` : "<span></span>"}
    <span class="muted">Page ${page} of ${Math.ceil(data.count / size)}</span>
    ${data.next ? `<a class="btn btn-ghost" href="${url(page + 1)}">Next →</a>` : "<span></span>"}
  </nav>`;
}

export function videoEmbed(url) {
  const yt = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]{11})/);
  if (yt) return `<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/${yt[1]}" title="Video" allowfullscreen loading="lazy"></iframe></div>`;
  if (/\.(mp4|webm|ogg)(\?|$)/i.test(url)) return `<video src="${esc(url)}" controls preload="metadata"></video>`;
  return `<p><a class="btn btn-ghost" href="${esc(url)}" target="_blank" rel="noopener">▶ Watch video</a></p>`;
}

// ---------- Forms ----------

export function field(name, label, { type = "text", value = "", required = true, attrs = "", options } = {}) {
  const req = required ? "required" : "";
  let input;
  if (type === "textarea") input = `<textarea name="${name}" rows="5" ${req} ${attrs}>${esc(value)}</textarea>`;
  else if (options) input = `<select name="${name}" ${req} ${attrs}>${options.map(([v, l]) => `<option value="${esc(v)}" ${v === value ? "selected" : ""}>${esc(l)}</option>`).join("")}</select>`;
  else input = `<input name="${name}" type="${type}" value="${esc(value)}" ${req} ${attrs}>`;
  return `<label class="field"><span>${esc(label)}</span>${input}</label>`;
}

const flatten = (msgs) => [].concat(msgs).flatMap((m) => (typeof m === "string" ? m : Object.values(m).flat())).join(" ");

/** Wires a form: disables the button while saving and shows API field errors next to inputs. */
export function onSubmit(form, handler) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const button = form.querySelector("button[type=submit], button:not([type])");
    form.querySelectorAll(".err, .form-alert").forEach((el) => el.remove());
    if (button) button.disabled = true;
    try {
      await handler(Object.fromEntries(new FormData(form)), form);
    } catch (err) {
      for (const [name, msgs] of Object.entries(err.data?.errors || {})) {
        const input = form.elements[name];
        if (input?.insertAdjacentHTML) input.insertAdjacentHTML("afterend", `<small class="err">${esc(flatten(msgs))}</small>`);
      }
      form.insertAdjacentHTML("afterbegin", `<div class="alert error form-alert">${esc(err.message)}</div>`);
    } finally {
      if (button) button.disabled = false;
    }
  });
}
