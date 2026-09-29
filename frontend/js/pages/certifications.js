import { page, api, esc, media, split, chips, empty, monthYear, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Certifications");
  const certs = await api("certificates/");
  app.innerHTML = `<section class="wrap section"><h1>Certifications</h1>
    <div class="grid">${certs.map((c) => `
      <a class="card card-link" href="certificate.html?id=${encodeURIComponent(c.credential_id)}">
        ${c.image ? `<img src="${esc(media(c.image))}" alt="" class="cover" loading="lazy">` : ""}
        <h3>${esc(c.name)}</h3><p class="muted">${esc(c.provider)} · ${monthYear(c.issue_date)}</p>
        ${chips(split(c.skills))}
      </a>`).join("") || empty("No certificates yet.")}</div>
  </section>`;
});
