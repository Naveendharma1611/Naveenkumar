// Runs student Python code inside a Web Worker via Pyodide (WASM CPython),
// completely in the browser — no backend execution server. Living in its own
// worker means a student's infinite loop freezes only this worker thread,
// not the page; src/lib/pyodideRunner.js terminates + replaces the worker if
// a run takes too long.

const PYODIDE_VERSION = "0.26.4";
importScripts(`https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`);

let pyodideReadyPromise = null;

async function getPyodide() {
  if (!pyodideReadyPromise) {
    pyodideReadyPromise = loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
    }).then(async (pyodide) => {
      // One reusable helper: executes `code` in a fresh module namespace with
      // `input()` fed from `stdin_text`, and returns captured stdout / any error.
      // A fresh namespace per call means no state leaks between test cases.
      await pyodide.runPythonAsync(`
import sys, io, types, traceback

def __npp_run(code, stdin_text):
    mod = types.ModuleType("solution")
    mod.__dict__["__name__"] = "__main__"
    stdin_lines = iter(stdin_text.split(chr(10)))

    def _input(prompt=""):
        try:
            return next(stdin_lines)
        except StopIteration:
            raise EOFError("EOF when reading a line")

    mod.__dict__["input"] = _input
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(code, "<student_code>", "exec"), mod.__dict__)
        return {"ok": True, "output": sys.stdout.getvalue(), "error": None}
    except Exception as e:
        return {
            "ok": False,
            "output": sys.stdout.getvalue(),
            "error": "".join(traceback.format_exception_only(type(e), e)).strip(),
        }
    finally:
        sys.stdout = old_stdout
`);
      return pyodide;
    });
  }
  return pyodideReadyPromise;
}

self.onmessage = async (event) => {
  const { requestId, code, tests } = event.data;
  try {
    const pyodide = await getPyodide();
    const runOne = pyodide.globals.get("__npp_run");
    const results = tests.map((t) => {
      const pyResult = runOne(code, t.stdin ?? "");
      const jsResult = pyResult.toJs({ dict_converter: Object.fromEntries });
      pyResult.destroy();
      const actual = (jsResult.output ?? "").trim();
      const expected = (t.expected ?? "").trim();
      return {
        id: t.id,
        stdin: t.stdin,
        expected,
        actual,
        error: jsResult.error,
        passed: jsResult.ok && actual === expected,
      };
    });
    self.postMessage({ requestId, ok: true, results });
  } catch (err) {
    self.postMessage({ requestId, ok: false, error: String(err && err.message ? err.message : err) });
  }
};
