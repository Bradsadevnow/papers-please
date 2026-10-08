import { useState } from 'react'
import { api } from '../api'

export default function ProbeBox({ selectedDocId }) {
  const [text, setText] = useState('')
  const [log, setLog] = useState([])
  const [asking, setAsking] = useState(false)

  async function handleAsk() {
    if (!text.trim() || asking) return
    const question = text.trim()
    setText('')
    setAsking(true)
    setLog((l) => [...l, { role: 'inspector', text: question }])
    try {
      const result = await api.probe(question, selectedDocId)
      setLog((l) => [...l, { role: 'gloss', text: result.content, tool_calls: result.tool_calls }])
    } finally {
      setAsking(false)
    }
  }

  return (
    <div className="panel probe">
      <h2>Probe GLOSS</h2>
      <div className="log">
        {log.map((entry, i) => (
          <div key={i} className={`entry ${entry.role}`}>
            <strong>{entry.role === 'inspector' ? 'You' : 'GLOSS'}</strong>
            <p>{entry.text}</p>
            {entry.tool_calls?.length > 0 && (
              <details>
                <summary>{entry.tool_calls.length} tool call(s)</summary>
                <ul>
                  {entry.tool_calls.map((c, j) => (
                    <li key={j}><code>{c.tool}({JSON.stringify(c.arguments)})</code></li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        ))}
        {asking && <div className="entry gloss muted">GLOSS is responding...</div>}
      </div>
      <div className="probe-form">
        <input
          placeholder="Ask a non-accusatory question..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
          disabled={asking}
        />
        <button onClick={handleAsk} disabled={asking || !text.trim()}>Ask</button>
      </div>
    </div>
  )
}
