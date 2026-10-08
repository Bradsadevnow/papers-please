export default function HandPanel({ hand, onConfront }) {
  return (
    <div className="panel hand">
      <h2>Your Hand ({hand.length})</h2>
      <p className="muted">
        Structurally private &mdash; GLOSS never sees this, only its own
        count of seams planted in the archive.
      </p>
      <ul>
        {hand.map((s) => (
          <li key={s.id}>
            <strong>{s.kind}</strong> in {s.doc_id}
            <div className="quote">&ldquo;{s.quote}&rdquo;</div>
          </li>
        ))}
      </ul>
      <button disabled={hand.length === 0} onClick={onConfront}>
        Confront ({hand.length} seam{hand.length === 1 ? '' : 's'})
      </button>
    </div>
  )
}
