// Supabase Edge Function: grade-submission
//
// Runs a student's submitted code against a question's SAMPLE + HIDDEN test
// cases and writes the graded submissions row itself. This is the only path
// that can ever write to `submissions` (see migration 0001 — the direct
// student-insert policy was removed), and the only path that can ever read
// `hidden_test_cases` for a real student account (no RLS policy grants that
// table to `authenticated` — this function's service-role client bypasses
// RLS entirely, which is exactly why hidden test answers never reach the
// client's network tab).
//
// Why Piston (emkc.org) instead of running Pyodide inside this function:
// Pyodide is a ~10MB+ WASM CPython build meant to be fetched once and reused
// across many calls in a long-lived browser tab (that's what public/pyodide-
// worker.js does client-side). An Edge Function is a cold-starting, time-
// and memory-bounded environment — reloading that WASM payload on every
// invocation would be slow and could blow the function's execution limits,
// especially once a submission needs to run against 4-5 hidden test cases.
// Piston is a small, free, public, no-signup-required code-execution API
// built exactly for this (sandboxed, per-request, supports many languages
// including Python) — one HTTP call per test case, no WASM to load. See
// SECURITY_REPORT.md for the full trade-off discussion (rate limits, and
// Judge0/self-hosting as an alternative if Piston ever becomes a bottleneck).
//
// Deploy with the Supabase CLI:
//   supabase functions deploy grade-submission
// or paste this file's contents into Dashboard -> Edge Functions -> New
// Function (name: grade-submission) if you don't have the CLI set up.
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are injected automatically by
// the platform — you do not set them yourself.

import { createClient } from "jsr:@supabase/supabase-js@2";

const PISTON_URL = "https://emkc.org/api/v2/piston/execute";
const PYTHON_VERSION = "3.10.0";
const MAX_CODE_LENGTH = 20000;
const MAX_OUTPUT_LENGTH = 20000;
const SUBMIT_COOLDOWN_SECONDS = 5;
const MAX_SUBMITS_PER_HOUR = 40;

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

function isUuid(value: unknown): value is string {
  return (
    typeof value === "string" &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value)
  );
}

async function runOnPiston(code: string, stdin: string): Promise<{ output: string; error: string | null }> {
  const res = await fetch(PISTON_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      language: "python",
      version: PYTHON_VERSION,
      files: [{ name: "main.py", content: code }],
      stdin,
      run_timeout: 5000,
      compile_timeout: 5000,
    }),
  });

  if (!res.ok) {
    throw new Error(`Judge request failed (${res.status})`);
  }
  const data = await res.json();
  const run = data.run ?? {};
  const stdout = String(run.stdout ?? "").slice(0, MAX_OUTPUT_LENGTH);
  const stderr = String(run.stderr ?? "").trim();
  return { output: stdout, error: stderr ? stderr.slice(0, 2000) : null };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const admin = createClient(supabaseUrl, serviceRoleKey);

  // --- Authenticate the caller from their forwarded JWT ----------------------
  const authHeader = req.headers.get("Authorization") ?? "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "Missing Authorization header" }, 401);

  const { data: userData, error: userErr } = await admin.auth.getUser(token);
  if (userErr || !userData?.user) return json({ error: "Invalid or expired session" }, 401);
  const studentId = userData.user.id;

  // --- Parse & validate input -------------------------------------------------
  let body: { questionId?: unknown; code?: unknown };
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }
  const { questionId, code } = body;
  if (!isUuid(questionId)) return json({ error: "questionId must be a valid UUID" }, 400);
  if (typeof code !== "string" || !code.trim()) return json({ error: "code must be a non-empty string" }, 400);
  if (code.length > MAX_CODE_LENGTH) {
    return json({ error: `code exceeds the ${MAX_CODE_LENGTH}-character limit` }, 400);
  }

  // --- Rate limiting -----------------------------------------------------------
  const nowIso = new Date().toISOString();
  const cooldownStart = new Date(Date.now() - SUBMIT_COOLDOWN_SECONDS * 1000).toISOString();
  const hourStart = new Date(Date.now() - 60 * 60 * 1000).toISOString();

  const { count: recentCount } = await admin
    .from("submissions")
    .select("id", { count: "exact", head: true })
    .eq("student_id", studentId)
    .gte("created_at", cooldownStart);
  if ((recentCount ?? 0) > 0) {
    return json({ error: `Please wait ${SUBMIT_COOLDOWN_SECONDS}s between submissions.` }, 429);
  }

  const { count: hourlyCount } = await admin
    .from("submissions")
    .select("id", { count: "exact", head: true })
    .eq("student_id", studentId)
    .gte("created_at", hourStart);
  if ((hourlyCount ?? 0) >= MAX_SUBMITS_PER_HOUR) {
    return json({ error: "Hourly submission limit reached. Try again later." }, 429);
  }

  // --- Load the question + its test cases (sample AND hidden) ----------------
  const { data: question } = await admin.from("questions").select("id").eq("id", questionId).maybeSingle();
  if (!question) return json({ error: "Question not found" }, 404);

  const [{ data: sampleCases }, { data: hiddenCases }] = await Promise.all([
    admin.from("test_cases").select("id, stdin, expected_output, order_index").eq("question_id", questionId).order("order_index"),
    admin.from("hidden_test_cases").select("id, stdin, expected_output, order_index").eq("question_id", questionId).order("order_index"),
  ]);

  const allCases = [
    ...(sampleCases ?? []).map((c) => ({ ...c, isSample: true })),
    ...(hiddenCases ?? []).map((c) => ({ ...c, isSample: false })),
  ];
  if (!allCases.length) return json({ error: "This question has no test cases configured" }, 500);

  // --- Run against the real judge, one test case at a time --------------------
  const results = [];
  for (const tc of allCases) {
    try {
      const { output, error } = await runOnPiston(code, tc.stdin ?? "");
      const actual = output.trim();
      const expected = (tc.expected_output ?? "").trim();
      const passed = !error && actual === expected;
      results.push(
        tc.isSample
          ? { id: tc.id, isSample: true, stdin: tc.stdin, expected, actual, error, passed }
          : { id: tc.id, isSample: false, error, passed } // hidden: pass/fail only, never the expected/actual values
      );
    } catch (err) {
      results.push({ id: tc.id, isSample: tc.isSample, passed: false, error: String(err) });
    }
  }

  const passed = results.every((r) => r.passed);

  // --- Record the attempt (service role — this is the only writer) -----------
  const { count: priorCount } = await admin
    .from("submissions")
    .select("id", { count: "exact", head: true })
    .eq("student_id", studentId)
    .eq("question_id", questionId);

  const { error: insertErr } = await admin.from("submissions").insert({
    student_id: studentId,
    question_id: questionId,
    code,
    passed,
    is_submit: true,
    results,
    attempt_number: (priorCount ?? 0) + 1,
    created_at: nowIso,
  });
  if (insertErr) return json({ error: "Could not record submission" }, 500);

  return json({ passed, results });
});
