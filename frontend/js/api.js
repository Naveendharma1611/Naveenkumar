// Talks to the Django REST API. Stores the JWT pair in localStorage and refreshes it on 401.
const API_URL = window.APP_CONFIG.API_URL.replace(/\/$/, "");
export const API_ORIGIN = new URL(API_URL).origin;

const store = {
  get(key) {
    try { return JSON.parse(localStorage.getItem(key)); } catch { return null; }
  },
  set(key, value) {
    try {
      if (value == null) localStorage.removeItem(key);
      else localStorage.setItem(key, JSON.stringify(value));
    } catch { /* storage blocked: stay logged out */ }
  },
};

export const auth = {
  get user() { return store.get("user"); },
  get access() { return store.get("access"); },
  get refresh() { return store.get("refresh"); },
  save({ user, access, refresh }) {
    if (user) store.set("user", user);
    if (access) store.set("access", access);
    if (refresh) store.set("refresh", refresh);
  },
  clear() { ["user", "access", "refresh"].forEach((k) => store.set(k, null)); },
  isStudent() { const u = this.user; return !!u && (u.role === "STUDENT" || u.is_admin); },
  isAdmin() { return !!this.user?.is_admin; },
};

export class ApiError extends Error {
  constructor(status, data) {
    super(data?.detail || `Request failed (${status})`);
    this.status = status;
    this.data = data;
  }
}

async function refreshTokens() {
  const refresh = auth.refresh;
  if (!refresh) return false;
  const res = await fetch(`${API_URL}/auth/refresh/`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ refresh }),
  }).catch(() => null);
  if (!res?.ok) { auth.clear(); return false; }
  auth.save(await res.json());
  return true;
}

export async function api(path, { method = "GET", body, retry = true } = {}) {
  const isForm = body instanceof FormData;
  const headers = {};
  if (body !== undefined && !isForm) headers["Content-Type"] = "application/json";
  if (auth.access) headers.Authorization = `Bearer ${auth.access}`;

  let res;
  try {
    res = await fetch(`${API_URL}/${path.replace(/^\//, "")}`, {
      method, headers, body: body === undefined ? undefined : isForm ? body : JSON.stringify(body),
    });
  } catch {
    throw new ApiError(0, { detail: `Can't reach the API at ${API_URL}. Is the Django server running?` });
  }

  // Expired access token: refresh once and retry (without a token if refresh failed).
  if (res.status === 401 && retry && headers.Authorization) {
    await refreshTokens();
    return api(path, { method, body, retry: false });
  }
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new ApiError(res.status, data);
  return data;
}
