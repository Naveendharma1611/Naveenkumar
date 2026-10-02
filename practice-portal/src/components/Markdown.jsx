import ReactMarkdown from "react-markdown";

// Shared prose styling for markdown-sourced topic explanations / question prompts.
export default function Markdown({ children }) {
  return (
    <div
      className="prose prose-slate max-w-none prose-pre:bg-slate-900 prose-pre:text-slate-100
        prose-code:text-brand-700 dark:prose-invert dark:prose-code:text-brand-300"
    >
      <ReactMarkdown>{children || ""}</ReactMarkdown>
    </div>
  );
}
