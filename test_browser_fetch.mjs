import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9226',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9226/json')
  const tabs = await tabsRes.json()
  const pageTab = tabs.find((t) => t.type === 'page') || tabs[0]

  const ws = new WebSocket(pageTab.webSocketDebuggerUrl)
  await new Promise((r) => (ws.onopen = r))

  let msgId = 1
  function send(method, params = {}) {
    return new Promise((resolve) => {
      const id = msgId++
      const handler = (event) => {
        const data = JSON.parse(event.data)
        if (data.id === id) {
          ws.removeEventListener('message', handler)
          resolve(data.result)
        }
      }
      ws.addEventListener('message', handler)
      ws.send(JSON.stringify({ id, method, params }))
    })
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.method === 'Runtime.consoleAPICalled') {
      console.log('CONSOLE:', data.params.type, data.params.args.map((a) => a.value || a.description))
    }
    if (data.method === 'Runtime.exceptionThrown') {
      console.error('EXCEPTION:', JSON.stringify(data.params.exceptionDetails, null, 2))
    }
    if (data.method === 'Network.responseReceived') {
      console.log('NETWORK RESPONSE:', data.params.response.url, data.params.response.status)
    }
  }

  await send('Runtime.enable')
  await send('Log.enable')
  await send('Network.enable')

  // Evaluate fetch directly from the browser window!
  const fetchTest = await send('Runtime.evaluate', {
    awaitPromise: true,
    expression: `
      (async () => {
        try {
          const res = await fetch("/api/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text: "Xin chào",
              voiceId: "hope"
            })
          });
          const text = await res.text();
          return { status: res.status, body: text };
        } catch (err) {
          return { error: err.message, stack: err.stack };
        }
      })()
    `,
  })
  console.log('Browser fetch test result:', fetchTest.result.value)

  ws.close()
} finally {
  chrome.kill()
}
