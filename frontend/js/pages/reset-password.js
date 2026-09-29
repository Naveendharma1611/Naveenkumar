import { page, api, ApiError, field, onSubmit, param, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Choose a new password");
  const uid = param("uid"), token = param("token");
  if (!uid || !token) throw new ApiError(400, { detail: "This reset link is incomplete. Request a new one from the Forgot password page." });
  app.innerHTML = `<section class="wrap section auth">
    <form class="card stack">
      <h1>Choose a new password</h1>
      ${field("new_password", "New password", { type: "password", attrs: "autocomplete=new-password minlength=8 autofocus" })}
      ${field("confirm", "Confirm new password", { type: "password", attrs: "autocomplete=new-password minlength=8" })}
      <button class="btn" type="submit">Save password</button>
    </form>
  </section>`;
  const form = app.querySelector("form");
  onSubmit(form, async ({ new_password, confirm }) => {
    if (new_password !== confirm) throw new ApiError(400, { detail: "Passwords don't match." });
    await api("auth/password-reset/confirm/", { method: "POST", body: { uid, token, new_password } });
    form.innerHTML = '<h1>Password updated</h1><p>You can now log in with your new password.</p><a class="btn" href="login.html">Log in</a>';
  });
});
