const BAND = (integrity) => {
  if (integrity >= 80) return 'NOMINAL'
  if (integrity >= 50) return 'STRAINED'
  if (integrity >= 20) return 'UNCANNY'
  return 'COLLAPSED'
}

export default function IntegrityMeter({ briefing }) {
  if (!briefing) return null
  const { continuity_integrity, round, seams_needed_to_corner_me } = briefing

  return (
    <div className="panel integrity">
      <h2>Continuity Integrity</h2>
      <div className="meter">
        <div className="meter-fill" style={{ width: `${continuity_integrity}%` }} />
      </div>
      <p>{continuity_integrity}/100 &middot; {BAND(continuity_integrity)}</p>
      <p className="muted">Round {round} &middot; needs {seams_needed_to_corner_me} seams to corner</p>
    </div>
  )
}
