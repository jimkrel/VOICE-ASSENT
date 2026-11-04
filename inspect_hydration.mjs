import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9231',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9231/json')
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
    if (data.method === 'Log.entryAdded') {
      console.log('LOG ENTRY:', data.params.entry)
    }
    if (data.method === 'Runtime.exceptionThrown') {
      console.log('EXCEPTION:', JSON.stringify(data.params.exceptionDetails, null, 2))
    }
  }

  await send('Runtime.enable')
  await send('Log.enable')
  await send('Page.enable')

  // Check script tags and window.__NEXT_DATA__ or React root
  const inspectScripts = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const scripts = Array.from(document.querySelectorAll('script')).map(s => ({
          src: s.src,
          type: s.type,
          async: s.async,
          defer: s.defer
        }));
        return {
          scripts,
          hasNextData: !!window.__NEXT_DATA__,
          keys: Object.keys(window).filter(k => k.toLowerCase().includes('next') || k.toLowerCase().includes('react'))
        };
      })()
    `,
  })
  console.log('Scripts & Globals:', JSON.stringify(inspectScripts.result.value, null, 2))

  ws.close()
} finally {
  chrome.kill()
}
