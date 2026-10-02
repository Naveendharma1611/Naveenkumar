import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import { useAuth } from "../../context/AuthContext";
import { logAdminAction } from "../../lib/adminLog";
import DifficultyBadge from "../../components/DifficultyBadge";
import AdminQuestionForm from "./AdminQuestionForm";

export default function AdminQuestions() {
  const { user } = useAuth();
  const [topics, setTopics] = useState([]);
  const [topicId, setTopicId] = useState("");
  const [questions, setQuestions] = useState([]);
  const [editing, setEditing] = useState(null); // { question, testCases } | "new" | null

  useEffect(() => {
    supabase
      .from("topics")
      .select("*")
      .order("order_index")
      .then(({ data }) => {
        setTopics(data || []);
        if (data?.length) setTopicId(data[0].id);
      });
  }, []);

  const loadQuestions = async (tid) => {
    const { data } = await supabase.from("questions").select("*").eq("topic_id", tid).order("order_index");
    setQuestions(data || []);
  };

  useEffect(() => {
    if (topicId) {
      setEditing(null);
      loadQuestions(topicId);
    }
  }, [topicId]);

  const startEdit = async (question) => {
    const [{ data: sampleCases }, { data: hiddenCases }] = await Promise.all([
      supabase.from("test_cases").select("*").eq("question_id", question.id).order("order_index"),
      supabase.from("hidden_test_cases").select("*").eq("question_id", question.id).order("order_index"),
    ]);
    const merged = [
      ...(sampleCases || []),
      ...(hiddenCases || []).map((tc) => ({ ...tc, is_sample: false })),
    ];
    setEditing({ question, testCases: merged });
  };

  const handleDelete = async (question) => {
    if (!confirm(`Delete "${question.title}"? This also deletes its test cases and submissions.`)) return;
    await supabase.from("questions").delete().eq("id", question.id);
    await logAdminAction(user.id, "delete", "questions", question.id, { title: question.title });
    loadQuestions(topicId);
  };

  const handleSaved = () => {
    setEditing(null);
    loadQuestions(topicId);
  };

  return (
    <div>
      <div className="flex flex-wrap items-center gap-3">
        <label className="label mb-0">Topic</label>
        <select className="input max-w-xs" value={topicId} onChange={(e) => setTopicId(e.target.value)}>
          {topics.map((t) => (
            <option key={t.id} value={t.id}>{t.title}</option>
          ))}
        </select>
        <button className="btn-primary ml-auto" onClick={() => setEditing("new")}>
          + Add question
        </button>
      </div>

      {editing && (
        <div className="mt-4">
          <AdminQuestionForm
            topicId={topicId}
            question={editing === "new" ? null : editing.question}
            testCases={editing === "new" ? [] : editing.testCases}
            onSaved={handleSaved}
            onCancel={() => setEditing(null)}
          />
        </div>
      )}

      <div className="mt-4 space-y-2">
        {questions.map((q) => (
          <div key={q.id} className="card flex items-center justify-between gap-3 p-4">
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-400">#{q.order_index}</span>
              <span className="font-medium">{q.title}</span>
              <DifficultyBadge difficulty={q.difficulty} />
              <span className="text-xs text-slate-400">{q.points} pts</span>
            </div>
            <div className="flex gap-2">
              <button className="btn-ghost" onClick={() => startEdit(q)}>Edit</button>
              <button className="btn-ghost text-rose-600" onClick={() => handleDelete(q)}>Delete</button>
            </div>
          </div>
        ))}
        {!questions.length && <p className="text-sm text-slate-500">No questions in this topic yet.</p>}
      </div>
    </div>
  );
}
