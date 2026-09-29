import { page, api, auth, ApiError, esc, media, field, onSubmit, toast, requireLogin, setTitle } from "../ui.js";

page(async (app) => {
  requireLogin();
  setTitle("Account");
  const me = await api("auth/me/");
  auth.save({ user: me });
  const sp = me.student_profile || {};
  const isStudent = me.role === "STUDENT";

  app.innerHTML = `<section class="wrap section narrow">
    <h1>Account settings</h1>
    <p class="muted">${esc(me.email)} · ${me.is_admin ? "Admin" : esc(me.role[0] + me.role.slice(1).toLowerCase())} · joined ${new Date(me.date_joined).toLocaleDateString()}</p>
    ${me.role === "VISITOR" ? `<div class="card"><h2>Become a student</h2>
      <p>Track completed lessons, bookmarks, notes and quiz scores.</p><button class="btn" id="upgrade">Upgrade to student</button></div>` : ""}
    <div class="grid two">
      <form class="card stack" id="profile-form"><h2>Profile</h2>
        ${field("full_name", "Full name", { value: me.full_name })}
        ${isStudent ? `
          ${field("phone", "Phone", { value: sp.phone, required: false })}
          ${field("institution", "Institution", { value: sp.institution, required: false })}
          ${field("course_of_study", "Course of study", { value: sp.course_of_study, required: false })}
          ${field("graduation_year", "Graduation year", { type: "number", value: sp.graduation_year ?? "", required: false, attrs: "min=1950 max=2100" })}
          ${field("interests", "Interests (comma separated)", { value: sp.interests, required: false })}
          ${field("bio", "Bio", { type: "textarea", value: sp.bio, required: false })}` : ""}
        <button class="btn" type="submit">Save profile</button>
      </form>
      <div class="stack">
        <form class="card stack" id="avatar-form"><h2>Photo</h2>
          <img id="avatar" class="avatar-lg" src="${esc(media(me.avatar) || "")}" alt="" ${me.avatar ? "" : "hidden"}>
          <input type="file" name="avatar" accept="image/*" required>
          <button class="btn btn-ghost" type="submit">Upload photo</button>
        </form>
        <form class="card stack" id="password-form"><h2>Change password</h2>
          ${field("current_password", "Current password", { type: "password", attrs: "autocomplete=current-password" })}
          ${field("new_password", "New password", { type: "password", attrs: "autocomplete=new-password minlength=8" })}
          ${field("confirm", "Confirm new password", { type: "password", attrs: "autocomplete=new-password minlength=8" })}
          <button class="btn" type="submit">Change password</button>
        </form>
      </div>
    </div>
  </section>`;

  app.querySelector("#upgrade")?.addEventListener("click", async () => {
    try {
      auth.save(await api("auth/upgrade-to-student/", { method: "POST" }));
      location.reload();
    } catch (err) { toast(err.message, "error"); }
  });

  onSubmit(app.querySelector("#profile-form"), async (d) => {
    const body = { full_name: d.full_name };
    if (isStudent) {
      body.student_profile = {
        phone: d.phone, institution: d.institution, course_of_study: d.course_of_study, interests: d.interests, bio: d.bio,
        graduation_year: d.graduation_year ? Number(d.graduation_year) : null,
      };
    }
    auth.save({ user: await api("auth/me/", { method: "PATCH", body }) });
    toast("Profile saved");
  });

  const avatarForm = app.querySelector("#avatar-form");
  onSubmit(avatarForm, async () => {
    const user = await api("auth/me/", { method: "PATCH", body: new FormData(avatarForm) });
    auth.save({ user });
    const img = app.querySelector("#avatar");
    img.src = media(user.avatar);
    img.hidden = false;
    toast("Photo updated");
  });

  const pwForm = app.querySelector("#password-form");
  onSubmit(pwForm, async ({ current_password, new_password, confirm }) => {
    if (new_password !== confirm) throw new ApiError(400, { detail: "New passwords don't match." });
    await api("auth/change-password/", { method: "POST", body: { current_password, new_password } });
    pwForm.reset();
    toast("Password changed");
  });
});
