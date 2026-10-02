import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { supabase } from "../lib/supabaseClient";
import { useAuth } from "../context/AuthContext";
import { FullPageSpinner } from "../components/RouteGuards";

export default function Dashboard() {
  const { user, profile } = useAuth();
  const [topics, setTopics] = useState(null);
  const [progress, setProgress] = useState({});

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const [{ data: topicRows }, { data: progressRows }] = await Promise.all([
        supabase.from("topics").select("*").order("order_index"),
        supabase.from("topic_progress").select("*").eq("student_id", user.id),
      ]);
      if (cancelled) return;
      setTopics(topicRows || []);
      const bySlug = {};
      (progressRows || []).forEach((p) => {
        bySlug[p.topic_slug] = p;
      });
      setProgress(bySlug);
    })();
    return () => {
      cancelled = true;
    };
  }, [user.id]);

  if (!topics) return <FullPageSpinner />;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-2xl font-bold">
        Welcome{profile?.full_name ? `, ${profile.full_name.split(" ")[0]}` : ""} 👋
      </h1>
      <p className="mt-1 text-slate-500 dark:text-slate-400">
        Work through each level in order — beginner to intermediate Python.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {topics.map((topic, idx) => {
          const p = progress[topic.slug];
          const total = p?.total_questions ?? 0;
          const solved = p?.solved_questions ?? 0;
          const pct = total ? Math.round((solved / total) * 100) : 0;
          return (
            <Link
              key={topic.id}
              to={`/topics/${topic.slug}`}
              className="card group flex flex-col gap-3 p-5 transition hover:border-brand-400 hover:shadow-md"
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400">
                    Level {idx + 1}
                  </span>
                  <h2 className="text-lg font-semibold group-hover:text-brand-600 dark:group-hover:text-brand-400">
                    {topic.title}
                  </h2>
                </div>
                {pct === 100 && total > 0 && <span className="text-xl" title="Completed">✅</span>}
              </div>

              <div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500 transition-all"
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  {solved}/{total} questions solved
                </p>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
