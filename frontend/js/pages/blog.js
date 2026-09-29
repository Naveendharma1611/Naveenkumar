import { page, api, esc, param, empty, pager, postCard, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Blog");
  const q = param("q"), category = param("category"), tag = param("tag"), pageNo = Number(param("page")) || 1, size = 9;
  const qs = new URLSearchParams({ page: pageNo, page_size: size });
  if (q) qs.set("search", q);
  if (category) qs.set("category__slug", category);
  if (tag) qs.set("tags__slug", tag);
  const [data, categories, tags] = await Promise.all([api(`blog/posts/?${qs}`), api("blog/categories/"), api("blog/tags/")]);
  app.innerHTML = `<section class="wrap section">
    <h1>Blog</h1>
    <form class="filters">
      <input name="q" value="${esc(q)}" placeholder="Search posts" aria-label="Search">
      <select name="category" aria-label="Category"><option value="">All categories</option>
        ${categories.map((c) => `<option value="${esc(c.slug)}" ${c.slug === category ? "selected" : ""}>${esc(c.name)}</option>`).join("")}</select>
      <button class="btn">Filter</button>
    </form>
    ${tags.length ? `<div class="chips">${tags.map((t) => `<a class="chip ${t.slug === tag ? "on" : ""}" href="blog.html?tag=${esc(t.slug)}">#${esc(t.name)}</a>`).join("")}</div>` : ""}
    <div class="grid">${data.results.map(postCard).join("") || empty("No posts yet.")}</div>
    ${pager(data, pageNo, size)}
  </section>`;
  app.querySelector("select").addEventListener("change", (e) => e.target.form.submit());
});
