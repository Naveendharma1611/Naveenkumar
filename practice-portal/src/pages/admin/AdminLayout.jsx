import { NavLink, Outlet } from "react-router-dom";

const tabClass = ({ isActive }) =>
  `rounded-lg px-3 py-2 text-sm font-medium transition ${
    isActive
      ? "bg-brand-600 text-white"
      : "bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
  }`;

export default function AdminLayout() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-2xl font-bold">Admin / Faculty</h1>
      <p className="mt-1 text-slate-500 dark:text-slate-400">
        Manage questions and review student progress.
      </p>

      <div className="mt-5 flex gap-2">
        <NavLink to="/admin" end className={tabClass}>
          Questions
        </NavLink>
        <NavLink to="/admin/students" className={tabClass}>
          Students
        </NavLink>
      </div>

      <div className="mt-6">
        <Outlet />
      </div>
    </div>
  );
}
