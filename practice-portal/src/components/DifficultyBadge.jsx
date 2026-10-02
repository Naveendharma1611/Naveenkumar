const CLASS_BY_DIFFICULTY = {
  easy: "badge-easy",
  medium: "badge-medium",
  hard: "badge-hard",
};

export default function DifficultyBadge({ difficulty }) {
  return (
    <span className={CLASS_BY_DIFFICULTY[difficulty] || "badge bg-slate-100 text-slate-700"}>
      {difficulty}
    </span>
  );
}
