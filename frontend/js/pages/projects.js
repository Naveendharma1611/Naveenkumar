import { page, api, esc, param, empty, pager, projectCard, setTitle } from "../ui.js";

const CATEGORIES = [["", "All categories"], ["PYTHON", "Python"], ["DATA_SCIENCE", "Data Science"], ["ML", "Machine Learning"],
  ["DL", "Deep Learning"], ["AI", "AI"], ["GENAI", "GenAI"], ["DJANGO", "Django"], ["ANALYTICS", "Data Analytics"], ["WEB", "Web Development"]];

page(async (app) => {
  setTitle("Projects");
  const q = param("q"), category = param("category"), pageNo = Number(param("page")) || 1, size = 12;
  const qs = new URLSearchParams({ page: pageNo, page_size: size });
  if (q) qs.set("search", q);
  if (category) qs.set("category", category);
  const data = await api(`projects/?${qs}`);
  app.innerHTML = `<section class="wrap section">
    <h1>Projects</h1>
    <form class="filters">
      <input name="q" value="${esc(q)}" placeholder="Search projects or technologies" aria-label="Search">
      <select name="category" aria-label="Category">${CATEGORIES.map(([v, l]) => `<option value="${v}" ${v === category ? "selected" : ""}>${l}</option>`).join("")}</select>
      <button class="btn">Filter</button>
    </form>
    <div class="grid">${data.results.map(projectCard).join("") || empty("No projects found.")}</div>
    ${pager(data, pageNo, size)}
  </section>`;
  app.querySelector("select").addEventListener("change", (e) => e.target.form.submit());
});
