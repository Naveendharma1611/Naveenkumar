import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { useTheme } from "../context/ThemeContext";

export default function CodeEditor({ value, onChange, height = "360px" }) {
  const { theme } = useTheme();
  return (
    <div className="overflow-hidden rounded-lg border border-slate-300 dark:border-slate-600">
      <CodeMirror
        value={value}
        height={height}
        theme={theme === "dark" ? "dark" : "light"}
        extensions={[python()]}
        onChange={onChange}
        basicSetup={{ tabSize: 4 }}
      />
    </div>
  );
}
