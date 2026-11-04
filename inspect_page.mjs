import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9225',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9225/json')
  const tabs = await tabsRes.json()
  const pageTab = tabs.find((t) => t.type === 'page') || tabs[0]
  console.log('Target tab:', pageTab.url)

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
      console.error('EXCEPTION:', data.params.exceptionDetails)
    }
  }

  await send('Runtime.enable')
  await send('Log.enable')
  await send('Page.enable')

  // Check page title and evaluate document.body.innerHTML
  const res = await send('Runtime.evaluate', {
    expression: 'document.title + " | " + document.querySelectorAll("button, a").length + " interactive elements"',
  })
  console.log('Page eval:', res.result.value)

  // Test finding the "Tạo giọng đọc" button
  const btnRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return 'Button not found';
        genBtn.click();
        return 'Clicked Tạo giọng đọc';
      })()
    `,
  })
  console.log('Button click result:', btnRes.result.value)

  // Wait 4 seconds to see console output or exceptions
  await new Promise((r) => setTimeout(r, 4000))

  const afterClick = await send('Runtime.evaluate', {
    expression: 'document.body.innerText.slice(0, 300)',
  })
  console.log('Page text after click:\n', afterClick.result.value)

  ws.close()
} finally {
  chrome.kill()
}
