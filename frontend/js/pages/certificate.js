import { page, api, esc, media, param, split, chips, fmtDate, setTitle } from "../ui.js";

page(async (app) => {
  const c = await api(`certificates/${encodeURIComponent(param("id"))}/`);
  setTitle(c.name, `${c.name} — ${c.provider}`);
  app.innerHTML = `<section class="wrap section narrow">
    <div class="alert success">✔ Verified certificate · ID ${esc(c.credential_id)}</div>
    <h1>${esc(c.name)}</h1>
    <p class="lead">${esc(c.provider)}</p>
    <p class="muted">Issued ${fmtDate(c.issue_date)}${c.expiry_date ? ` · Expires ${fmtDate(c.expiry_date)}` : ""}</p>
    ${c.image ? `<img src="${esc(media(c.image))}" alt="${esc(c.name)}" class="cover-lg">` : ""}
    <p>${esc(c.description)}</p>
    ${chips(split(c.skills))}
    <div class="actions">
      ${c.credential_url ? `<a class="btn" href="${esc(c.credential_url)}" target="_blank" rel="noopener">Verify with provider</a>` : ""}
      ${c.pdf ? `<a class="btn btn-ghost" href="${esc(media(c.pdf))}" target="_blank" rel="noopener">Download PDF</a>` : ""}
    </div>
  </section>`;
});
