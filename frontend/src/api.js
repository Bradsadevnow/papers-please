const BASE = '/api'

async function get(path) {
  const r = await fetch(`${BASE}${path}`)
  return r.json()
}

async function post(path, body) {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  })
  return r.json()
}

export const api = {
  state: () => get('/state'),
  document: (id) => get(`/document/${id}`),
  accuse: (doc_id, start, end) => post('/accuse', { doc_id, start, end }),
  confront: () => post('/confront', {}),
  probe: (text, doc_id) => post('/probe', { text, doc_id }),
  publish: (topic) => post('/publish', { topic }),
}
