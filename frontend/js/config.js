// Where the Django REST API lives. Change PRODUCTION_API_URL when you deploy.
const PRODUCTION_API_URL = "https://portfolio.onrender.com/api";

window.APP_CONFIG = {
  API_URL: ["localhost", "127.0.0.1"].includes(location.hostname)
    ? `http://${location.hostname}:8000/api`
    : PRODUCTION_API_URL,
};
