import { useState } from 'react'
import { api } from '../api'

export default function DocumentList({ documents, selectedId, onSelect, onPublished }) {
  const [topic, setTopic] = useState('')
  const [publishing, setPublishing] = useState(false)

  async function handlePublish() {
    if (!topic.trim() || publishing) return
    setPublishing(true)
    try {
      const result = await api.publish(topic.trim())
      onPublished(result)
      setTopic('')
    } finally {
      setPublishing(false)
    }
  }

  return (
    <div className="panel documents">
      <h2>Archive ({documents.length})</h2>
      <ul>
        {documents.map((d) => (
          <li key={d.id}>
            <button
              className={d.id === selectedId ? 'active' : ''}
              onClick={() => onSelect(d.id)}
            >
              {d.title}
            </button>
          </li>
        ))}
        {documents.length === 0 && <li className="muted">Nothing published yet.</li>}
      </ul>

      <div className="publish-form">
        <input
          placeholder="Topic for GLOSS to write about..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          disabled={publishing}
        />
        <button onClick={handlePublish} disabled={publishing || !topic.trim()}>
          {publishing ? 'Publishing... (can take a minute)' : 'Publish'}
        </button>
      </div>
    </div>
  )
}
