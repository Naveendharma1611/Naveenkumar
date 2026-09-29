import { page, api, auth, field, onSubmit, nextPage, homeFor, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Create account");
  if (auth.user) return location.replace(homeFor(auth.user));
  app.innerHTML = `<section class="wrap section auth">
    <form class="card stack">
      <h1>Create account</h1>
      ${field("full_name", "Full name", { attrs: "autocomplete=name autofocus" })}
      ${field("email", "Email", { type: "email", attrs: "autocomplete=email" })}
      ${field("role", "I am a", { value: "STUDENT", options: [["STUDENT", "Student — track lessons, notes and quizzes"], ["VISITOR", "Visitor — just browsing"]] })}
      ${field("password", "Password", { type: "password", attrs: "autocomplete=new-password minlength=8" })}
      ${field("password_confirm", "Confirm password", { type: "password", attrs: "autocomplete=new-password minlength=8" })}
      <button class="btn" type="submit">Register</button>
      <p class="muted">Already have an account? <a href="login.html">Log in</a></p>
    </form>
  </section>`;
  onSubmit(app.querySelector("form"), async (data) => {
    const res = await api("auth/register/", { method: "POST", body: data });
    auth.save(res);
    location.href = nextPage(homeFor(res.user));
  });
});
