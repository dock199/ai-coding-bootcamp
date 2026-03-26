interface ReportEditorProps {
  value: string;
  onChange: (value: string) => void;
}

export function ReportEditor({ value, onChange }: ReportEditorProps) {
  if (!value) return null;

  return (
    <div className="report-editor">
      <label htmlFor="report-textarea" className="report-editor__label">
        生成された日報
      </label>
      <textarea
        id="report-textarea"
        className="report-editor__textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={16}
        spellCheck={false}
      />
    </div>
  );
}
