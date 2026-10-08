// Main-thread wrapper around public/pyodide-worker.js. Runs student code
// against a list of {id, stdin, expected} test cases and resolves with
// per-test {id, stdin, expected, actual, passed, error}. If a run exceeds
// `timeoutMs` (student code stuck in an infinite loop, say), the worker is
// terminated and replaced so the page never freezes — the caller gets a
// clear timeout result instead of hanging forever.

const RUN_TIMEOUT_MS = 10000;

let worker = null;
let nextRequestId = 1;
const pending = new Map();

function createWorker() {
  const w = new Worker(`${import.meta.env.BASE_URL}pyodide-worker.js`);
  w.onmessage = (event) => {
    const { requestId, ok, results, error } = event.data;
    const entry = pending.get(requestId);
    if (!entry) return;
    pending.delete(requestId);
    clearTimeout(entry.timer);
    if (ok) entry.resolve(results);
    else entry.reject(new Error(error || "Python execution failed."));
  };
  w.onerror = (event) => {
    // A worker-level crash fails every pending request on this worker.
    for (const [id, entry] of pending) {
      clearTimeout(entry.timer);
      entry.reject(new Error(event.message || "The Python runner crashed."));
      pending.delete(id);
    }
    resetWorker();
  };
  return w;
}

function resetWorker() {
  try {
    worker?.terminate();
  } catch {
    /* ignore */
  }
  worker = createWorker();
}

function getWorker() {
  if (!worker) worker = createWorker();
  return worker;
}

/**
 * @param {string} code student's Python source
 * @param {{id:string, stdin:string, expected:string}[]} tests
 * @returns {Promise<{id:string, stdin:string, expected:string, actual:string, passed:boolean, error:string|null}[]>}
 */
export function runTests(code, tests, { timeoutMs = RUN_TIMEOUT_MS } = {}) {
  const requestId = nextRequestId++;
  const w = getWorker();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(requestId);
      resetWorker();
      reject(new Error(`Timed out after ${Math.round(timeoutMs / 1000)}s — check for an infinite loop.`));
    }, timeoutMs);
    pending.set(requestId, { resolve, reject, timer });
    w.postMessage({ requestId, code, tests });
  });
}

// Kick off loading Pyodide in the background (e.g. as soon as the question
// page mounts) so the student's first Run doesn't pay the full load cost.
export function warmUpRunner() {
  runTests("pass", [{ id: "__warmup__", stdin: "", expected: "" }]).catch(() => {
    /* warm-up failures are silent; the real run will surface the error */
  });
}
