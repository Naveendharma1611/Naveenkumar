// Markup shared by several pages.
import { esc, md, media, monthYear, chips, split } from "./ui.js";

const cap = (s) => (s ? s[0] + s.slice(1).toLowerCase() : "");
// "2020 – 2024", "Mar 2021 – Present", just "2024" when only the end is known, or nothing at all.
const period = (start, end, fmt) => (start ? `${fmt(start)} – ${end ? fmt(end) : "Present"}` : end ? fmt(end) : "");
const meta = (...parts) => {
  const text = parts.filter(Boolean).map((x) => esc(x)).join(" · ");
  return text ? `<br><small class="muted">${text}</small>` : "";
};

// Complete study-material pages (static HTML), keyed by study topic slug, in display order.
// A backend topic with the same slug is shown through this card instead of its own card.
export const NOTES = {
  "data-science": {
    href: "data-science-material.html", title: "📊 Data Science Complete Study Material",
    text: "Data science end to end in 32 modules: statistics, SQL, data cleaning, EDA, visualization, machine learning, responsible AI, deployment and projects.",
  },
  java: {
    href: "java-material.html", title: "☕ Java Complete End-to-End Study Material",
    text: "Java from fundamentals to professional development in 74 modules: OOP, collections, modern Java, concurrency, JDBC, Spring Boot, REST, security, microservices, Docker, cloud and projects.",
  },
  numpy: {
    href: "numpy-material.html", title: "🔢 NumPy Complete Study Material",
    text: "NumPy end to end in 39 modules: arrays, indexing, broadcasting, statistics, linear algebra, data science and machine learning, with examples, practice and projects.",
  },
  python: {
    href: "python-material.html", title: "🐍 Python Complete Study Material",
    text: "All of Python in 20 modules: basics, data types, loops, functions, OOP, file handling and exceptions, with code examples and interview tips.",
  },
  c: {
    href: "c-material.html", title: "💻 C Programming Complete Study Material",
    text: "Beginner to advanced C in 23 modules: operators, loops, functions, arrays, strings, pointers, dynamic memory, structures, files and more, with examples and practice questions.",
  },
  cpp: {
    href: "cpp-material.html", title: "⚙️ C++ Complete Study Material",
    text: "C++ end to end in 24 modules: OOP, templates, STL containers and algorithms, lambdas, smart pointers, move semantics, multithreading and CMake, with projects and interview prep.",
  },
  html: {
    href: "html-material.html", title: "🌐 HTML Complete Study Material",
    text: "HTML end to end in 19 modules: text, links, media, tables, forms, semantic HTML, SEO, accessibility, HTML5 APIs, responsive design and deployment, with projects.",
  },
  css: {
    href: "css-material.html", title: "🎨 CSS Complete Study Material",
    text: "CSS end to end in 20 modules: selectors, box model, Flexbox, Grid, responsive design, animations, variables, modern CSS and best practices, with projects.",
  },
  sql: {
    href: "sql-material.html", title: "🗃️ SQL Zero to Hero",
    text: "SQL in order across 24 modules: tables, queries, joins, subqueries, CTEs, window functions, transactions, design and performance — every query with its real result.",
  },
  django: {
    href: "django-material.html", title: "🌿 Django Zero to Hero",
    text: "Build a complete blog in 24 modules: URLs, views, templates, ORM, admin, forms, auth, REST APIs, testing, security, caching and deployment.",
  },
};

// The title link stretches over the whole card; `extra` can hold a second link (e.g. to lessons).
export const notesCard = (n, extra = "") => `
  <article class="card card-link featured-card">
    <span class="badge">Complete notes</span>
    <h3><a class="card-main-link" href="${n.href}">${n.title}</a></h3>
    <p class="muted">${n.text}</p>
    ${extra}
  </article>`;

export const jobsList = (jobs) => (jobs.length ? `<ul class="timeline">${jobs.map((j) => `
  <li><strong>${esc(j.role)}</strong> — ${esc(j.organization)} <span class="badge">${cap(j.type)}</span>
    ${meta(period(j.start_date, j.end_date, monthYear), j.location)}
    <div class="prose">${md(j.description)}</div>${chips(split(j.technologies))}</li>`).join("")}</ul>`
  : '<p class="muted">No experience added yet.</p>');

export const educationList = (items) => `<ul class="timeline">${items.map((e) => `
  <li><strong>${esc(e.degree)}</strong> — ${esc(e.institution)}${e.location ? `, ${esc(e.location)}` : ""}
    ${meta(period(e.start_year, e.end_year, String), e.score)}
    ${e.description ? `<p class="muted">${esc(e.description)}</p>` : ""}</li>`).join("")}</ul>`;

export function materialItem(m) {
  const href = media(m.file || m.external_url);
  const next = encodeURIComponent(location.pathname.split("/").pop() + location.search);
  return `<p class="material">📎 <strong>${esc(m.title)}</strong> <span class="badge">${esc(m.kind_label)}</span>
    ${href ? `<a href="${esc(href)}" target="_blank" rel="noopener">Open</a>`
      : m.requires_login ? `<a href="login.html?next=${next}">Log in to access</a>` : ""}
    ${m.description ? `<br><small class="muted">${esc(m.description)}</small>` : ""}</p>`;
}
