import { page, api, esc, param, route, setTitle } from "../ui.js";

page(async (app) => {
  const q = param("q").trim();
  setTitle(q ? `Search: ${q}` : "Search");
  const data = q.length >= 2 ? await api(`search/?q=${encodeURIComponent(q)}`) : { groups: [] };
  const groups = data.groups.filter((g) => g.results.length);
  app.innerHTML = `<section class="wrap section narrow">
    <h1>Search</h1>
    <form class="filters"><input name="q" value="${esc(q)}" placeholder="Search projects, lessons, blog, interview questions" aria-label="Search" autofocus>
      <button class="btn">Search</button></form>
    ${groups.map((g) => `<h2>${esc(g.label)}</h2>${g.results.map((r) => `
      <a class="card card-link" href="${esc(route(r.url))}"><strong>${esc(r.title)}</strong>
        ${r.subtitle ? `<p class="muted">${esc(r.subtitle.slice(0, 160))}</p>` : ""}</a>`).join("")}`).join("")
      || `<p class="muted">${q.length >= 2 ? `No results for “${esc(q)}”.` : "Type at least 2 characters."}</p>`}
  </section>`;
});
