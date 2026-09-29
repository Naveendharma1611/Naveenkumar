import { page, api, auth, field, onSubmit, nextPage, homeFor, param, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Log in");
  if (auth.user) return location.replace(nextPage(homeFor(auth.user)));
  const next = param("next") ? `?next=${encodeURIComponent(param("next"))}` : "";
  app.innerHTML = `<section class="wrap section auth">
    <form class="card stack">
      <h1>Log in</h1>
      ${field("email", "Email", { type: "email", attrs: "autocomplete=email autofocus" })}
      ${field("password", "Password", { type: "password", attrs: "autocomplete=current-password" })}
      <button class="btn" type="submit">Log in</button>
      <a href="forgot-password.html" class="muted">Forgot password?</a>
      <p class="muted">New here? <a href="register.html${next}">Create an account</a></p>
    </form>
  </section>`;
  onSubmit(app.querySelector("form"), async (data) => {
    const res = await api("auth/login/", { method: "POST", body: data });
    auth.save(res);
    location.href = nextPage(homeFor(res.user));
  });
});
