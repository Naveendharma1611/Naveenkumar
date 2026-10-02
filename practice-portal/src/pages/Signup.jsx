import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Logo from "../components/Logo";

export default function Signup() {
  const { signUp } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    fullName: "",
    rollNumber: "",
    department: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setNotice("");
    setBusy(true);
    try {
      const { session } = await signUp(form);
      if (session) {
        navigate("/", { replace: true });
      } else {
        setNotice("Account created — check your email to confirm it, then log in.");
      }
    } catch (err) {
      setError(err.message || "Could not sign up.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-8">
      <div className="mb-6 flex justify-center">
        <Logo />
      </div>
      <div className="card p-6">
        <h1 className="mb-1 text-xl font-bold">Create your account</h1>
        <p className="mb-6 text-sm text-slate-500 dark:text-slate-400">
          Start practicing Python in minutes.
        </p>

        {error && (
          <div className="mb-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
            {error}
          </div>
        )}
        {notice && (
          <div className="mb-4 rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300">
            {notice}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label" htmlFor="fullName">Full name</label>
            <input id="fullName" required className="input" value={form.fullName} onChange={update("fullName")} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label" htmlFor="rollNumber">Roll number</label>
              <input id="rollNumber" required className="input" value={form.rollNumber} onChange={update("rollNumber")} />
            </div>
            <div>
              <label className="label" htmlFor="department">Department</label>
              <input id="department" required className="input" value={form.department} onChange={update("department")} />
            </div>
          </div>
          <div>
            <label className="label" htmlFor="email">College email</label>
            <input id="email" type="email" required className="input" value={form.email} onChange={update("email")} />
          </div>
          <div>
            <label className="label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              minLength={6}
              className="input"
              value={form.password}
              onChange={update("password")}
            />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={busy}>
            {busy ? "Creating account…" : "Sign up"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate-500 dark:text-slate-400">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
