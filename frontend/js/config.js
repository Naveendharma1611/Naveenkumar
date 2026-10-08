// Where the Django REST API lives. Live Render Backend URL:
const PRODUCTION_API_URL = "https://naveenkumar-qelp.onrender.com/api";

const urlParams = typeof window !== "undefined" && window.location ? new URLSearchParams(window.location.search) : null;
const apiParam = urlParams ? urlParams.get("api") : null;
if (apiParam) {
  try { localStorage.setItem("CUSTOM_API_URL", apiParam.replace(/\/$/, "")); } catch (e) {}
}

const savedApi = typeof localStorage !== "undefined" ? localStorage.getItem("CUSTOM_API_URL") : null;

window.APP_CONFIG = {
  API_URL: ["localhost", "127.0.0.1"].includes(location.hostname)
    ? `http://${location.hostname}:8000/api`
    : (savedApi || PRODUCTION_API_URL),
};

