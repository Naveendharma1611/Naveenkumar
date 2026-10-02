import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { supabase, MAX_ATTEMPTS_BEFORE_HELP } from "../lib/supabaseClient";
import { useAuth } from "../context/AuthContext";
import { runTests, warmUpRunner } from "../lib/pyodideRunner";
import { FullPageSpinner } from "../components/RouteGuards";
import Markdown from "../components/Markdown";
import DifficultyBadge from "../components/DifficultyBadge";
import CodeEditor from "../components/CodeEditor";
import ResultsPanel from "../components/ResultsPanel";

const draftKey = (questionId) => `npp-draft-${questionId}`;

export default function QuestionPage() {
  const { slug, questionId } = useParams();
  const { user } = useAuth();

  const [question, setQuestion] = useState(null);
  const [testCases, setTestCases] = useState([]);
  const [siblings, setSiblings] = useState([]);
  const [code, setCode] = useState("");
  const [results, setResults] = useState(null);
  const [resultsKind, setResultsKind] = useState("run"); // "run" | "submit"
  const [failedAttempts, setFailedAttempts] = useState(0);
  const [solved, setSolved] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setResults(null);
    setShowHint(false);
    setShowSolution(false);

    const { data: q } = await supabase.from("questions").select("*").eq("id", questionId).single();
    if (!q) return;
    const [{ data: cases }, { data: topicRow }, { data: pastSubmits }] = await Promise.all([
      supabase.from("test_cases").select("*").eq("question_id", questionId).order("order_index"),
      supabase.from("topics").select("id").eq("slug", slug).single(),
      supabase
        .from("submissions")
        .select("passed")
        .eq("student_id", user.id)
        .eq("question_id", questionId)
        .eq("is_submit", true),
    ]);

    setQuestion(q);
    setTestCases(cases || []);
    setFailedAttempts((pastSubmits || []).filter((s) => !s.passed).length);
    setSolved((pastSubmits || []).some((s) => s.passed));

    if (topicRow) {
      const { data: siblingRows } = await supabase
        .from("questions")
        .select("id, title, order_index")
        .eq("topic_id", topicRow.id)
        .order("order_index");
      setSiblings(siblingRows || []);
    }

    const draft = localStorage.getItem(draftKey(questionId));
    setCode(draft ?? q.starter_code ?? "");
    warmUpRunner();
  }, [questionId, slug, user.id]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    if (question) localStorage.setItem(draftKey(questionId), code);
  }, [code, questionId, question]);

  const sampleCases = useMemo(() => testCases.filter((t) => t.is_sample), [testCases]);
  const nextQuestion = useMemo(() => {
    const idx = siblings.findIndex((s) => s.id === questionId);
    return idx >= 0 ? siblings[idx + 1] : null;
  }, [siblings, questionId]);

  const canSeeHelp = failedAttempts >= MAX_ATTEMPTS_BEFORE_HELP;

  const toRunnerTests = (cases) =>
    cases.map((c) => ({ id: c.id, stdin: c.stdin, expected: c.expected_output, isSample: c.is_sample }));

  const handleRun = async () => {
    setError("");
    setBusy(true);
    setResultsKind("run");
    try {
      const outcome = await runTests(code, toRunnerTests(sampleCases));
      setResults(outcome.map((r, i) => ({ ...r, isSample: sampleCases[i]?.is_sample })));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  const handleSubmit = async () => {
    setError("");
    setBusy(true);
    setResultsKind("submit");
    try {
      const all = toRunnerTests(testCases);
      const outcome = await runTests(code, all);
      const merged = outcome.map((r, i) => ({ ...r, isSample: testCases[i]?.is_sample }));
      setResults(merged);
      const passed = merged.every((r) => r.passed);

      const { count } = await supabase
        .from("submissions")
        .select("id", { count: "exact", head: true })
        .eq("student_id", user.id)
        .eq("question_id", questionId)
        .eq("is_submit", true);

      await supabase.from("submissions").insert({
        student_id: user.id,
        question_id: questionId,
        code,
        passed,
        is_submit: true,
        results: merged,
        attempt_number: (count || 0) + 1,
      });

      if (passed) {
        setSolved(true);
      } else {
        setFailedAttempts((n) => n + 1);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  if (!question) return <FullPageSpinner />;

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <Link to={`/topics/${slug}`} className="text-sm text-brand-600 hover:underline dark:text-brand-400">
        ← Back to topic
      </Link>

      <div className="mt-2 flex flex-wrap items-center gap-2">
        <h1 className="text-xl font-bold">{question.title}</h1>
        <DifficultyBadge difficulty={question.difficulty} />
        <span className="text-xs text-slate-400">{question.points} pts</span>
        {solved && (
          <span className="badge bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300">
            ✓ Solved
          </span>
        )}
      </div>

      <div className="mt-4 grid gap-6 lg:grid-cols-2">
        <div>
          <div className="card p-5">
            <Markdown>{question.prompt}</Markdown>
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            <button
              className="btn-ghost"
              onClick={() => setShowHint((s) => !s)}
              disabled={!canSeeHelp}
              title={canSeeHelp ? "" : `Unlocks after ${MAX_ATTEMPTS_BEFORE_HELP} failed submissions`}
            >
              💡 {canSeeHelp ? (showHint ? "Hide hint" : "Show hint") : `Hint (after ${MAX_ATTEMPTS_BEFORE_HELP} fails)`}
            </button>
            <button
              className="btn-ghost"
              onClick={() => setShowSolution((s) => !s)}
              disabled={!canSeeHelp}
              title={canSeeHelp ? "" : `Unlocks after ${MAX_ATTEMPTS_BEFORE_HELP} failed submissions`}
            >
              🔓 {canSeeHelp ? (showSolution ? "Hide solution" : "Show solution") : "Solution (locked)"}
            </button>
          </div>

          {canSeeHelp && showHint && (
            <div className="mt-3 rounded-lg bg-amber-50 p-3 text-sm text-amber-800 dark:bg-amber-900/20 dark:text-amber-200">
              {question.hint || "No hint provided for this question."}
            </div>
          )}
          {canSeeHelp && showSolution && (
            <pre className="mt-3 overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-100">
              <code>{question.solution_code}</code>
            </pre>
          )}
        </div>

        <div>
          <CodeEditor value={code} onChange={setCode} />

          <div className="mt-3 flex flex-wrap gap-2">
            <button className="btn-secondary" onClick={handleRun} disabled={busy}>
              {busy && resultsKind === "run" ? "Running…" : "▶ Run"}
            </button>
            <button className="btn-primary" onClick={handleSubmit} disabled={busy}>
              {busy && resultsKind === "submit" ? "Submitting…" : "Submit"}
            </button>
            <button
              className="btn-ghost"
              onClick={() => setCode(question.starter_code || "")}
              disabled={busy}
              title="Reset to starter code"
            >
              ↺ Reset
            </button>
            {nextQuestion && (
              <Link to={`/topics/${slug}/questions/${nextQuestion.id}`} className="btn-ghost ml-auto">
                Next question →
              </Link>
            )}
          </div>

          {error && (
            <div className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
              {error}
            </div>
          )}

          <ResultsPanel results={results} title={resultsKind === "run" ? "Sample test results" : "Submission results"} />
        </div>
      </div>
    </div>
  );
}
