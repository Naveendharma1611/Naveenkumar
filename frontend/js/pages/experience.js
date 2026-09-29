import { page, api, setTitle } from "../ui.js";
import { educationList, jobsList } from "../parts.js";

page(async (app) => {
  setTitle("Experience");
  const [jobs, education] = await Promise.all([api("experience/"), api("education/")]);
  app.innerHTML = `<section class="wrap section narrow">
    <h1>Experience</h1>${jobsList(jobs)}
    ${education.length ? `<h2>Education</h2>${educationList(education)}` : ""}
  </section>`;
});
