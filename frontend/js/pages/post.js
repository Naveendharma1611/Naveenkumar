import { page, api, esc, md, media, param, fmtDate, setTitle } from "../ui.js";

page(async (app) => {
  const p = await api(`blog/posts/${encodeURIComponent(param("slug"))}/`);
  setTitle(p.title, p.excerpt);
  const meta = [fmtDate(p.published_at), `${p.reading_minutes} min read`, p.author_name, p.category?.name].filter(Boolean).map(esc).join(" · ");
  app.innerHTML = `<article class="wrap section narrow">
    <a href="blog.html" class="muted">← All posts</a>
    <h1>${esc(p.title)}</h1>
    <p class="muted">${meta}</p>
    ${p.featured_image ? `<img src="${esc(media(p.featured_image))}" alt="" class="cover-lg">` : ""}
    <div class="prose">${md(p.content)}</div>
    <div class="chips">${p.tags.map((t) => `<a class="chip" href="blog.html?tag=${esc(t.slug)}">#${esc(t.name)}</a>`).join("")}</div>
  </article>`;
});
