import { page, api, esc, field, onSubmit, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Reset password");
  app.innerHTML = `<section class="wrap section auth">
    <form class="card stack">
      <h1>Reset password</h1>
      <p class="muted">Enter your email and we'll send you a reset link.</p>
      ${field("email", "Email", { type: "email", attrs: "autocomplete=email autofocus" })}
      <button class="btn" type="submit">Send reset link</button>
      <a href="login.html" class="muted">Back to log in</a>
    </form>
  </section>`;
  const form = app.querySelector("form");
  onSubmit(form, async (data) => {
    const res = await api("auth/password-reset/", { method: "POST", body: data });
    form.innerHTML = `<h1>Check your email</h1><p>${esc(res?.detail || "If that email has an account, a reset link is on its way.")}</p>
      <a class="btn" href="login.html">Back to log in</a>`;
  });
});
