import { useEffect, useState } from "react";
import * as XLSX from "xlsx";
import { supabase } from "../../lib/supabaseClient";

export default function AdminStudents() {
  const [rows, setRows] = useState(null);

  useEffect(() => {
    supabase
      .from("leaderboard")
      .select("*")
      .then(({ data }) => setRows(data || []));
  }, []);

  const exportToExcel = () => {
    const sheetData = rows.map((r, idx) => ({
      Rank: idx + 1,
      Name: r.full_name,
      "Roll Number": r.roll_number,
      Department: r.department,
      "Questions Solved": r.solved_count,
      Score: r.score,
    }));
    const worksheet = XLSX.utils.json_to_sheet(sheetData);
    worksheet["!cols"] = [{ wch: 6 }, { wch: 24 }, { wch: 16 }, { wch: 20 }, { wch: 16 }, { wch: 10 }];
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Student Progress");
    const date = new Date().toISOString().slice(0, 10);
    XLSX.writeFile(workbook, `nk-practice-portal-results-${date}.xlsx`);
  };

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Student progress</h2>
        <button className="btn-primary" onClick={exportToExcel} disabled={!rows?.length}>
          ⬇ Export to Excel
        </button>
      </div>

      <div className="card mt-4 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500 dark:bg-slate-900/50 dark:text-slate-400">
            <tr>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Roll number</th>
              <th className="px-4 py-3">Department</th>
              <th className="px-4 py-3 text-right">Solved</th>
              <th className="px-4 py-3 text-right">Score</th>
            </tr>
          </thead>
          <tbody>
            {(rows || []).map((r) => (
              <tr key={r.student_id} className="border-t border-slate-100 dark:border-slate-700">
                <td className="px-4 py-3">{r.full_name}</td>
                <td className="px-4 py-3">{r.roll_number}</td>
                <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{r.department}</td>
                <td className="px-4 py-3 text-right">{r.solved_count}</td>
                <td className="px-4 py-3 text-right font-semibold">{r.score}</td>
              </tr>
            ))}
            {rows && !rows.length && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-slate-400">No students yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
