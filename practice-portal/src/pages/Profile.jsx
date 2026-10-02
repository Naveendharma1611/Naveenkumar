import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";
import { useAuth } from "../context/AuthContext";
import { FullPageSpinner } from "../components/RouteGuards";

function computeStreak(dateStrings) {
  // dateStrings: "YYYY-MM-DD" values the student solved at least one question on.
  const days = new Set(dateStrings);
  if (!days.size) return 0;

  const toKey = (d) => d.toISOString().slice(0, 10);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let cursor = new Date(today);
  if (!days.has(toKey(cursor))) {
    cursor.setDate(cursor.getDate() - 1); // streak can still be "alive" if yesterday counts
    if (!days.has(toKey(cursor))) return 0;
  }

  let streak = 0;
  while (days.has(toKey(cursor))) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return streak;
}

export default function Profile() {
  const { user, profile } = useAuth();
  const [stats, setStats] = useState(null);
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    (async () => {
      const [{ data: lbRow }, { data: solvedRows }, { data: progressRows }] = await Promise.all([
        supabase.from("leaderboard").select("*").eq("student_id", user.id).maybeSingle(),
        supabase.from("solved_questions").select("solved_at").eq("student_id", user.id),
        supabase.from("topic_progress").select("*, topics:topic_id(title, order_index)").eq("student_id", user.id),
      ]);

      const dayStrings = (solvedRows || []).map((r) => new Date(r.solved_at).toISOString().slice(0, 10));
      setStats({
        score: lbRow?.score ?? 0,
        solvedCount: lbRow?.solved_count ?? 0,
        streak: computeStreak(dayStrings),
      });
      setTopics((progressRows || []).sort((a, b) => (a.topics?.order_index ?? 0) - (b.topics?.order_index ?? 0)));
    })();
  }, [user.id]);

  if (!stats) return <FullPageSpinner />;

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-2xl font-bold">{profile?.full_name}</h1>
      <p className="text-slate-500 dark:text-slate-400">
        {profile?.roll_number} · {profile?.department}
      </p>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <StatCard label="Score" value={stats.score} icon="⭐" />
        <StatCard label="Solved" value={stats.solvedCount} icon="✅" />
        <StatCard label="Day streak" value={stats.streak} icon="🔥" />
      </div>

      <h2 className="mt-8 mb-3 text-lg font-semibold">Progress by topic</h2>
      <div className="space-y-2">
        {topics.map((t) => {
          const total = t.total_questions || 0;
          const solved = t.solved_questions || 0;
          const pct = total ? Math.round((solved / total) * 100) : 0;
          return (
            <div key={t.topic_id} className="card p-4">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{t.topics?.title}</span>
                <span className="text-slate-500 dark:text-slate-400">{solved}/{total}</span>
              </div>
              <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div className="card p-4 text-center">
      <div className="text-2xl">{icon}</div>
      <div className="mt-1 text-2xl font-bold">{value}</div>
      <div className="text-xs text-slate-500 dark:text-slate-400">{label}</div>
    </div>
  );
}
