import { useRef, useState } from 'react'
import { api } from '../api'

function selectionOffsets(container) {
  const sel = window.getSelection()
  if (!sel.rangeCount) return null
  const range = sel.getRangeAt(0)
  if (range.collapsed) return null

  const preRange = document.createRange()
  preRange.selectNodeContents(container)
  preRange.setEnd(range.startContainer, range.startOffset)
  const start = preRange.toString().length
  const end = start + range.toString().length
  return { start, end }
}

export default function DocumentReader({ doc, onAccused }) {
  const bodyRef = useRef(null)
  const [flash, setFlash] = useState(null)

  if (!doc) {
    return (
      <div className="panel reader empty">
        <p className="muted">Select a document to read it.</p>
      </div>
    )
  }

  async function handleMouseUp() {
    const offsets = selectionOffsets(bodyRef.current)
    if (!offsets) return
    const result = await api.accuse(doc.id, offsets.start, offsets.end)
    window.getSelection().removeAllRanges()
    setFlash(result.found ? 'found' : 'miss')
    setTimeout(() => setFlash(null), 900)
    if (result.found) onAccused(result)
  }

  return (
    <div className={`panel reader ${flash ?? ''}`}>
      <h2>{doc.title}</h2>
      <p className="muted">Highlight text to claim it as a seam.</p>
      <pre ref={bodyRef} onMouseUp={handleMouseUp}>{doc.body}</pre>
    </div>
  )
}
