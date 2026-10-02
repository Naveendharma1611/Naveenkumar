import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { supabase } from "../lib/supabaseClient";
import { useAuth } from "../context/AuthContext";
import { FullPageSpinner } from "../components/RouteGuards";
import Markdown from "../components/Markdown";
import DifficultyBadge from "../components/DifficultyBadge";

export default function TopicPage() {
  const { slug } = useParams();
  const { user } = useAuth();
  const [topic, setTopic] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [solvedIds, setSolvedIds] = useState(new Set());
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setTopic(null);
    setNotFound(false);
    (async () => {
      const { data: topicRow } = await supabase.from("topics").select("*").eq("slug", slug).single();
      if (cancelled) return;
      if (!topicRow) {
        setNotFound(true);
        return;
      }
      const [{ data: questionRows }, { data: solvedRows }] = await Promise.all([
        supabase.from("questions").select("*").eq("topic_id", topicRow.id).order("order_index"),
        supabase.from("solved_questions").select("question_id").eq("student_id", user.id).eq("topic_id", topicRow.id),
      ]);
      if (cancelled) return;
      setTopic(topicRow);
      setQuestions(questionRows || []);
      setSolvedIds(new Set((solvedRows || []).map((r) => r.question_id)));
    })();
    return () => {
      cancelled = true;
    };
  }, [slug, user.id]);

  if (notFound) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-12 text-center">
        <p className="text-slate-500">Topic not found.</p>
        <Link to="/" className="btn-primary mt-4 inline-flex">Back to topics</Link>
      </div>
    );
  }
  if (!topic) return <FullPageSpinner />;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <Link to="/" className="text-sm text-brand-600 hover:underline dark:text-brand-400">← All topics</Link>
      <h1 className="mt-2 text-2xl font-bold">{topic.title}</h1>

      <div className="card mt-4 p-5">
        <Markdown>{topic.explanation}</Markdown>
        <div className="mt-4">
          <p className="mb-1 text-sm font-semibold text-slate-500 dark:text-slate-400">Example</p>
          <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-100">
            <code>{topic.example_code}</code>
          </pre>
          {topic.example_output && (
            <div className="mt-2 rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-700/50">
              <p className="mb-1 text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Output</p>
              <pre className="whitespace-pre-wrap">{topic.example_output}</pre>
            </div>
          )}
        </div>
      </div>

      <h2 className="mt-8 mb-3 text-lg font-semibold">Practice questions</h2>
      <div className="space-y-2">
        {questions.map((q, idx) => {
          const solved = solvedIds.has(q.id);
          return (
            <Link
              key={q.id}
              to={`/topics/${slug}/questions/${q.id}`}
              className="card flex items-center justify-between gap-3 p-4 transition hover:border-brand-400"
            >
              <div className="flex items-center gap-3">
                <span
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-semibold ${
                    solved
                      ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300"
                      : "bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-300"
                  }`}
                >
                  {solved ? "✓" : idx + 1}
                </span>
                <span className="font-medium">{q.title}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">{q.points} pts</span>
                <DifficultyBadge difficulty={q.difficulty} />
              </div>
            </Link>
          );
        })}
        {!questions.length && <p className="text-sm text-slate-500">No questions yet for this topic.</p>}
      </div>
    </div>
  );
}
