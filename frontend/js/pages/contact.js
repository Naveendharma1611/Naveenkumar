import { page, api, esc, field, onSubmit, getProfile, setTitle } from "../ui.js";

const openedAt = Date.now();

page(async (app) => {
  setTitle("Contact");
  const p = await getProfile();
  app.innerHTML = `<section class="wrap section narrow">
    <h1>Contact me</h1>
    <p class="lead">Have a question, opportunity or project in mind? Send a message.</p>
    <div class="grid two">
      <form class="card stack">
        ${field("name", "Name")}
        ${field("email", "Email", { type: "email" })}
        ${field("subject", "Subject")}
        ${field("message", "Message", { type: "textarea" })}
        <div class="visually-hidden" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
        <button class="btn" type="submit">Send message</button>
      </form>
      <div class="card">
        ${p.email ? `<p>✉ <a href="mailto:${esc(p.email)}">${esc(p.email)}</a></p>` : ""}
        ${p.phone ? `<p>☎ ${esc(p.phone)}</p>` : ""}
        ${p.location ? `<p>📍 ${esc(p.location)}</p>` : ""}
        ${p.linkedin_url ? `<p><a href="${esc(p.linkedin_url)}" target="_blank" rel="noopener">LinkedIn</a></p>` : ""}
        ${p.github_url ? `<p><a href="${esc(p.github_url)}" target="_blank" rel="noopener">GitHub</a></p>` : ""}
        <p class="muted">I usually reply within a couple of days.</p>
      </div>
    </div>
  </section>`;
  const form = app.querySelector("form");
  onSubmit(form, async (data) => {
    const res = await api("contact/", { method: "POST", body: { ...data, elapsed_ms: Date.now() - openedAt } });
    form.reset();
    form.insertAdjacentHTML("afterbegin", `<div class="alert success form-alert">${esc(res.detail)}</div>`);
  });
});
