export default function ConfrontationResult({ result, onDismiss }) {
  if (!result) return null
  const { outcome, narration } = result

  return (
    <div className={`overlay outcome-${outcome}`}>
      <div className="outcome-card">
        <h2>{outcome.toUpperCase()}</h2>
        {narration?.content && <p>{narration.content}</p>}
        <button onClick={onDismiss}>Continue</button>
      </div>
    </div>
  )
}
