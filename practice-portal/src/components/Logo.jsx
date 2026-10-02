export default function Logo({ size = "md" }) {
  const box = size === "sm" ? "h-7 w-7 text-sm" : "h-9 w-9 text-base";
  const text = size === "sm" ? "text-base" : "text-lg";
  return (
    <div className="flex items-center gap-2">
      <div
        className={`flex ${box} items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 font-bold text-white shadow-sm`}
        aria-hidden="true"
      >
        NK
      </div>
      <span className={`${text} font-bold tracking-tight text-slate-900 dark:text-white`}>
        Practice Portal
      </span>
    </div>
  );
}
