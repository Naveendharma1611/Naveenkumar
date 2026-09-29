import { page, setTitle } from "../ui.js";

page(async (app) => {
  setTitle("Not found");
  app.innerHTML = `<section class="wrap section auth"><div class="card">
    <h1>404 — Page not found</h1><p>The page you are looking for doesn't exist.</p>
    <a class="btn" href="index.html">Go home</a></div></section>`;
});
