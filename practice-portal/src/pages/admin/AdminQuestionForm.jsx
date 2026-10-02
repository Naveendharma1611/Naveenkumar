import { useState } from "react";
import { supabase, DIFFICULTY_POINTS } from "../../lib/supabaseClient";
import { useAuth } from "../../context/AuthContext";
import { logAdminAction } from "../../lib/adminLog";

const emptyTestCase = (isSample = false) => ({
  localId: crypto.randomUUID(),
  stdin: "",
  expected_output: "",
  is_sample: isSample,
});

function toFormState(question, testCases) {
  if (question) {
    return {
      title: question.title,
      prompt: question.prompt,
      difficulty: question.difficulty,
      points: question.points,
      starter_code: question.starter_code,
      hint: question.hint,
      solution_code: question.solution_code,
      order_index: question.order_index,
      testCases: testCases.length
        ? testCases.map((t) => ({ localId: t.id, ...t }))
        : [emptyTestCase(true), emptyTestCase()],
    };
  }
  return {
    title: "",
    prompt: "",
    difficulty: "easy",
    points: DIFFICULTY_POINTS.easy,
    starter_code: "# Write your code here\n",
    hint: "",
    solution_code: "",
    order_index: 1,
    testCases: [emptyTestCase(true), emptyTestCase()],
  };
}

export default function AdminQuestionForm({ topicId, question, testCases, onSaved, onCancel }) {
  const { user } = useAuth();
  const [form, setForm] = useState(() => toFormState(question, testCases || []));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const setDifficulty = (e) => {
    const difficulty = e.target.value;
    setForm((f) => ({ ...f, difficulty, points: DIFFICULTY_POINTS[difficulty] ?? f.points }));
  };

  const updateCase = (localId, key, value) =>
    setForm((f) => ({
      ...f,
      testCases: f.testCases.map((tc) => (tc.localId === localId ? { ...tc, [key]: value } : tc)),
    }));

  const addCase = () => setForm((f) => ({ ...f, testCases: [...f.testCases, emptyTestCase()] }));
  const removeCase = (localId) =>
    setForm((f) => ({ ...f, testCases: f.testCases.filter((tc) => tc.localId !== localId) }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.title.trim() || !form.prompt.trim()) {
      setError("Title and prompt are required.");
      return;
    }
    if (!Number.isFinite(Number(form.points)) || Number(form.points) <= 0) {
      setError("Points must be a positive number.");
      return;
    }
    if (!form.testCases.some((tc) => tc.is_sample)) {
      setError("At least one test case must be marked as sample (shown to students).");
      return;
    }
    if (!form.testCases.some((tc) => !tc.is_sample)) {
      setError("Add at least one hidden test case — grading relies on them, not just the sample.");
      return;
    }
    if (form.testCases.some((tc) => !tc.expected_output.trim())) {
      setError("Every test case needs an expected output.");
      return;
    }

    setBusy(true);
    try {
      const payload = {
        topic_id: topicId,
        title: form.title,
        prompt: form.prompt,
        difficulty: form.difficulty,
        points: Number(form.points),
        starter_code: form.starter_code,
        hint: form.hint,
        solution_code: form.solution_code,
        order_index: Number(form.order_index),
      };

      let questionId = question?.id;
      let action = "create";
      if (questionId) {
        action = "update";
        const { error: updateErr } = await supabase.from("questions").update(payload).eq("id", questionId);
        if (updateErr) throw updateErr;
        await Promise.all([
          supabase.from("test_cases").delete().eq("question_id", questionId),
          supabase.from("hidden_test_cases").delete().eq("question_id", questionId),
        ]);
      } else {
        const { data, error: insertErr } = await supabase.from("questions").insert(payload).select().single();
        if (insertErr) throw insertErr;
        questionId = data.id;
      }

      const sampleRows = form.testCases
        .filter((tc) => tc.is_sample)
        .map((tc, idx) => ({
          question_id: questionId,
          stdin: tc.stdin,
          expected_output: tc.expected_output,
          is_sample: true,
          order_index: idx,
        }));
      const hiddenRows = form.testCases
        .filter((tc) => !tc.is_sample)
        .map((tc, idx) => ({
          question_id: questionId,
          stdin: tc.stdin,
          expected_output: tc.expected_output,
          order_index: idx,
        }));

      const [{ error: sampleErr }, { error: hiddenErr }] = await Promise.all([
        sampleRows.length ? supabase.from("test_cases").insert(sampleRows) : { error: null },
        hiddenRows.length ? supabase.from("hidden_test_cases").insert(hiddenRows) : { error: null },
      ]);
      if (sampleErr) throw sampleErr;
      if (hiddenErr) throw hiddenErr;

      await logAdminAction(user.id, action, "questions", questionId, {
        title: form.title,
        sample_count: sampleRows.length,
        hidden_count: hiddenRows.length,
      });

      onSaved();
    } catch (err) {
      setError(err.message || "Could not save the question.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card space-y-4 p-5">
      <h3 className="text-lg font-semibold">{question ? "Edit question" : "New question"}</h3>
      {error && (
        <div className="rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
          {error}
        </div>
      )}

      <div>
        <label className="label">Title</label>
        <input className="input" required value={form.title} onChange={set("title")} />
      </div>

      <div>
        <label className="label">Prompt (markdown)</label>
        <textarea className="input font-mono" rows={6} required value={form.prompt} onChange={set("prompt")} />
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="label">Difficulty</label>
          <select className="input" value={form.difficulty} onChange={setDifficulty}>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div>
          <label className="label">Points</label>
          <input type="number" className="input" value={form.points} onChange={set("points")} />
        </div>
        <div>
          <label className="label">Order</label>
          <input type="number" className="input" value={form.order_index} onChange={set("order_index")} />
        </div>
      </div>

      <div>
        <label className="label">Starter code</label>
        <textarea className="input font-mono" rows={4} value={form.starter_code} onChange={set("starter_code")} />
      </div>
      <div>
        <label className="label">Hint</label>
        <textarea className="input" rows={2} value={form.hint} onChange={set("hint")} />
      </div>
      <div>
        <label className="label">Solution code</label>
        <textarea className="input font-mono" rows={6} value={form.solution_code} onChange={set("solution_code")} />
      </div>

      <div>
        <div className="mb-2 flex items-center justify-between">
          <label className="label mb-0">Test cases</label>
          <button type="button" className="btn-ghost" onClick={addCase}>+ Add test case</button>
        </div>
        <div className="space-y-3">
          {form.testCases.map((tc) => (
            <div key={tc.localId} className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
              <div className="grid gap-2 sm:grid-cols-2">
                <div>
                  <label className="label">stdin</label>
                  <textarea
                    className="input font-mono"
                    rows={2}
                    value={tc.stdin}
                    onChange={(e) => updateCase(tc.localId, "stdin", e.target.value)}
                  />
                </div>
                <div>
                  <label className="label">expected output</label>
                  <textarea
                    className="input font-mono"
                    rows={2}
                    value={tc.expected_output}
                    onChange={(e) => updateCase(tc.localId, "expected_output", e.target.value)}
                  />
                </div>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={tc.is_sample}
                    onChange={(e) => updateCase(tc.localId, "is_sample", e.target.checked)}
                  />
                  Sample (visible to students)
                </label>
                <button type="button" className="text-sm text-rose-600 hover:underline" onClick={() => removeCase(tc.localId)}>
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-2">
        <button type="submit" className="btn-primary" disabled={busy}>
          {busy ? "Saving…" : "Save question"}
        </button>
        <button type="button" className="btn-secondary" onClick={onCancel} disabled={busy}>
          Cancel
        </button>
      </div>
    </form>
  );
}
