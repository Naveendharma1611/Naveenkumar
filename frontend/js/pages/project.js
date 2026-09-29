import { page, api, esc, md, media, param, chips, videoEmbed, setTitle } from "../ui.js";

const SECTIONS = [["problem_statement", "Problem statement"], ["objective", "Objective"], ["dataset", "Dataset"],
  ["architecture", "Architecture"], ["data_flow", "Data flow"], ["algorithm", "Algorithm"], ["implementation", "Implementation"],
  ["model_training", "Model training"], ["evaluation", "Evaluation"], ["results", "Results"],
  ["future_improvements", "Future improvements"], ["documentation", "Documentation"]];

page(async (app) => {
  const p = await api(`projects/${encodeURIComponent(param("slug"))}/`);
  setTitle(p.title, p.summary);
  const model = media(p.model_3d);
  const viewable = model && /\.(glb|gltf)(\?|$)/i.test(model);
  app.innerHTML = `<article class="wrap section narrow">
    <a href="projects.html" class="muted">← All projects</a>
    <p><span class="badge">${esc(p.category_label)}</span> ${p.is_sample ? '<span class="badge">Sample</span>' : ""}</p>
    <h1>${esc(p.title)}</h1>
    <p class="lead">${esc(p.summary)}</p>
    ${chips(p.technologies.map((t) => t.name))}
    <div class="actions">
      ${p.github_url ? `<a class="btn" href="${esc(p.github_url)}" target="_blank" rel="noopener">GitHub</a>` : ""}
      ${p.live_demo_url ? `<a class="btn btn-ghost" href="${esc(p.live_demo_url)}" target="_blank" rel="noopener">Live demo</a>` : ""}
      ${p.documentation_pdf ? `<a class="btn btn-ghost" href="${esc(media(p.documentation_pdf))}" target="_blank" rel="noopener">Documentation PDF</a>` : ""}
    </div>
    ${p.cover_image ? `<img src="${esc(media(p.cover_image))}" alt="${esc(p.title)}" class="cover-lg">` : ""}
    ${p.pipeline_steps.length ? `<h2>Pipeline</h2><ol class="pipeline">${p.pipeline_steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>` : ""}
    ${SECTIONS.filter(([f]) => p[f]).map(([f, label]) => `<h2>${label}</h2><div class="prose">${md(p[f])}</div>`).join("")}
    ${p.images.length ? `<h2>Screenshots</h2><div class="grid">${p.images.map((i) => `
      <figure><img src="${esc(media(i.image))}" alt="${esc(i.alt_text || i.caption)}" loading="lazy"><figcaption class="muted">${esc(i.caption)}</figcaption></figure>`).join("")}</div>` : ""}
    ${p.demo_video_url || p.videos.length ? `<h2>Videos</h2>${p.demo_video_url ? videoEmbed(p.demo_video_url) : ""}
      ${p.videos.map((v) => (v.video ? `<video src="${esc(media(v.video))}" controls preload="metadata"></video>` : videoEmbed(v.url))).join("")}` : ""}
    ${model ? `<h2>3D model</h2>${viewable ? `<model-viewer src="${esc(model)}" camera-controls auto-rotate class="model" alt="3D model of ${esc(p.title)}"></model-viewer>` : ""}
      <p><a href="${esc(model)}" download>Download model</a></p>` : ""}
    ${p.code_snippets.length ? `<h2>Code</h2>${p.code_snippets.map((s) => `<h3>${esc(s.title)}</h3><pre><code class="language-${esc(s.language)}">${esc(s.code)}</code></pre>`).join("")}` : ""}
  </article>`;
  if (viewable) import("https://cdn.jsdelivr.net/npm/@google/model-viewer@4/dist/model-viewer.min.js");
});
