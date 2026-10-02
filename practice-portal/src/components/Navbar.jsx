import { NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import Logo from "./Logo";
import ThemeToggle from "./ThemeToggle";
import { useAuth } from "../context/AuthContext";

const linkClass = ({ isActive }) =>
  `rounded-lg px-3 py-2 text-sm font-medium transition ${
    isActive
      ? "bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300"
      : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
  }`;

export default function Navbar() {
  const { user, profile, isAdmin, signOut } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    navigate("/login");
  };

  const links = user
    ? [
        ["/", "Topics"],
        ["/leaderboard", "Leaderboard"],
        ["/profile", "Profile"],
        ...(isAdmin ? [["/admin", "Admin"]] : []),
      ]
    : [];

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-700 dark:bg-slate-900/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <NavLink to="/" className="shrink-0">
          <Logo />
        </NavLink>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === "/"} className={linkClass}>
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          <ThemeToggle />
          {user ? (
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-600 dark:text-slate-300">
                {profile?.full_name || "Student"}
              </span>
              <button className="btn-secondary" onClick={handleSignOut}>
                Log out
              </button>
            </div>
          ) : (
            <>
              <NavLink to="/login" className="btn-ghost">
                Log in
              </NavLink>
              <NavLink to="/signup" className="btn-primary">
                Sign up
              </NavLink>
            </>
          )}
        </div>

        <button
          className="btn-ghost md:hidden"
          aria-label="Toggle menu"
          onClick={() => setOpen((o) => !o)}
        >
          ☰
        </button>
      </div>

      {open && (
        <div className="border-t border-slate-200 px-4 pb-3 md:hidden dark:border-slate-700">
          <div className="flex flex-col gap-1 pt-2">
            {links.map(([to, label]) => (
              <NavLink key={to} to={to} end={to === "/"} className={linkClass} onClick={() => setOpen(false)}>
                {label}
              </NavLink>
            ))}
            <div className="mt-2 flex items-center justify-between">
              <ThemeToggle />
              {user ? (
                <button className="btn-secondary" onClick={handleSignOut}>
                  Log out
                </button>
              ) : (
                <div className="flex gap-2">
                  <NavLink to="/login" className="btn-ghost" onClick={() => setOpen(false)}>
                    Log in
                  </NavLink>
                  <NavLink to="/signup" className="btn-primary" onClick={() => setOpen(false)}>
                    Sign up
                  </NavLink>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
