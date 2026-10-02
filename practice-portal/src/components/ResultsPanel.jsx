export default function ResultsPanel({ results, title }) {
  if (!results?.length) return null;
  const passedCount = results.filter((r) => r.passed).length;

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{title}</h3>
        <span
          className={`badge ${
            passedCount === results.length
              ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300"
              : "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300"
          }`}
        >
          {passedCount}/{results.length} passed
        </span>
      </div>

      {results.map((r, idx) => (
        <div
          key={r.id ?? idx}
          className={`rounded-lg border p-3 text-sm ${
            r.passed
              ? "border-emerald-200 bg-emerald-50 dark:border-emerald-900 dark:bg-emerald-900/20"
              : "border-rose-200 bg-rose-50 dark:border-rose-900 dark:bg-rose-900/20"
          }`}
        >
          <div className="mb-2 flex items-center justify-between">
            <span className="font-medium">
              {r.passed ? "✅" : "❌"} Test case {idx + 1}
              {r.isSample && <span className="ml-2 text-xs text-slate-400">(sample)</span>}
            </span>
          </div>
          {r.error ? (
            <pre className="whitespace-pre-wrap text-rose-700 dark:text-rose-300">{r.error}</pre>
          ) : r.expected === undefined ? (
            // Hidden test case: the judge only ever returns pass/fail for these,
            // never the expected/actual values, so there's nothing to leak here.
            <p className="text-slate-500 dark:text-slate-400">
              Hidden test case — {r.passed ? "passed." : "did not match the expected output."}
            </p>
          ) : (
            <div className="grid gap-2 sm:grid-cols-2">
              {r.stdin && (
                <div>
                  <p className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Input</p>
                  <pre className="whitespace-pre-wrap rounded bg-white/60 p-2 dark:bg-slate-900/40">{r.stdin}</pre>
                </div>
              )}
              <div>
                <p className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Expected</p>
                <pre className="whitespace-pre-wrap rounded bg-white/60 p-2 dark:bg-slate-900/40">{r.expected}</pre>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Your output</p>
                <pre className="whitespace-pre-wrap rounded bg-white/60 p-2 dark:bg-slate-900/40">{r.actual || "(empty)"}</pre>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
