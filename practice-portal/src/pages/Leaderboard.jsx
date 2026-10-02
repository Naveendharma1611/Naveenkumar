import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";
import { useAuth } from "../context/AuthContext";
import { FullPageSpinner } from "../components/RouteGuards";

const MEDALS = ["🥇", "🥈", "🥉"];

export default function Leaderboard() {
  const { user } = useAuth();
  const [rows, setRows] = useState(null);

  useEffect(() => {
    supabase
      .from("leaderboard")
      .select("*")
      .limit(100)
      .then(({ data }) => setRows(data || []));
  }, []);

  if (!rows) return <FullPageSpinner />;

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-2xl font-bold">🏆 College Leaderboard</h1>
      <p className="mt-1 text-slate-500 dark:text-slate-400">Ranked by total points from solved questions.</p>

      <div className="card mt-6 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500 dark:bg-slate-900/50 dark:text-slate-400">
            <tr>
              <th className="px-4 py-3">Rank</th>
              <th className="px-4 py-3">Student</th>
              <th className="px-4 py-3">Department</th>
              <th className="px-4 py-3 text-right">Solved</th>
              <th className="px-4 py-3 text-right">Score</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, idx) => (
              <tr
                key={r.student_id}
                className={`border-t border-slate-100 dark:border-slate-700 ${
                  r.student_id === user.id ? "bg-brand-50 dark:bg-brand-900/20" : ""
                }`}
              >
                <td className="px-4 py-3 font-semibold">{MEDALS[idx] || idx + 1}</td>
                <td className="px-4 py-3">
                  {r.full_name}
                  <div className="text-xs text-slate-400">{r.roll_number}</div>
                </td>
                <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{r.department}</td>
                <td className="px-4 py-3 text-right">{r.solved_count}</td>
                <td className="px-4 py-3 text-right font-bold text-brand-600 dark:text-brand-400">{r.score}</td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-slate-400">
                  No one has solved a question yet — be the first!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
