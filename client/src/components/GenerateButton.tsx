interface GenerateButtonProps {
  onClick: () => void;
  disabled: boolean;
  isLoading: boolean;
}

export function GenerateButton({ onClick, disabled, isLoading }: GenerateButtonProps) {
  return (
    <button
      type="button"
      className="generate-button"
      onClick={onClick}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
    >
      {isLoading ? (
        <>
          <span className="generate-button__spinner" aria-hidden="true" />
          生成中…
        </>
      ) : (
        '日報を生成'
      )}
    </button>
  );
}
