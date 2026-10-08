import { useEffect, useState } from 'react'
import { api } from './api'
import DocumentList from './components/DocumentList'
import DocumentReader from './components/DocumentReader'
import HandPanel from './components/HandPanel'
import IntegrityMeter from './components/IntegrityMeter'
import ProbeBox from './components/ProbeBox'
import ConfrontationResult from './components/ConfrontationResult'
import './App.css'

export default function App() {
  const [state, setState] = useState(null)
  const [selectedId, setSelectedId] = useState(null)
  const [selectedDoc, setSelectedDoc] = useState(null)
  const [confrontResult, setConfrontResult] = useState(null)

  async function refreshState() {
    setState(await api.state())
  }

  useEffect(() => { refreshState() }, [])

  useEffect(() => {
    if (!selectedId) { setSelectedDoc(null); return }
    api.document(selectedId).then(setSelectedDoc)
  }, [selectedId])

  async function handleConfront() {
    const result = await api.confront()
    setConfrontResult(result)
    setState(result.state)
  }

  function handleDismissOutcome() {
    setConfrontResult(null)
  }

  async function handlePublished(result) {
    setState(result.state)
    setSelectedId(result.document.id)
  }

  function handleAccused() {
    refreshState()
  }

  if (!state) return <div className="loading">Loading GLOSS's archive...</div>

  return (
    <div className="app">
      <header>
        <h1>Papers, Please — Inspecting MERIDIAN</h1>
      </header>
      <div className="layout">
        <aside className="left">
          <DocumentList
            documents={state.documents}
            selectedId={selectedId}
            onSelect={setSelectedId}
            onPublished={handlePublished}
          />
          <IntegrityMeter briefing={state.briefing} />
          <HandPanel hand={state.hand} onConfront={handleConfront} />
        </aside>
        <main className="center">
          <DocumentReader doc={selectedDoc} onAccused={handleAccused} />
        </main>
        <aside className="right">
          <ProbeBox selectedDocId={selectedId} />
        </aside>
      </div>
      <ConfrontationResult result={confrontResult} onDismiss={handleDismissOutcome} />
    </div>
  )
}
