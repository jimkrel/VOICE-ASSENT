import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9228',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9228/json')
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

  let requestMade = false
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.method === 'Network.requestWillBeSent') {
      console.log('NETWORK REQ:', data.params.request.method, data.params.request.url)
      if (data.params.request.url.includes('/api/tts')) requestMade = true
    }
    if (data.method === 'Runtime.consoleAPICalled') {
      console.log('CONSOLE:', data.params.type, data.params.args.map((a) => a.value || a.description))
    }
  }

  await send('Runtime.enable')
  await send('Network.enable')

  // Use CDP Input.dispatchMouseEvent to simulate REAL human click at the button's exact x,y coordinates!
  const box = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        const rect = genBtn.getBoundingClientRect();
        return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
      })()
    `,
  })
  console.log('Click coordinates:', box.result.value)

  // Real mouse move & click
  await send('Input.dispatchMouseEvent', {
    type: 'mouseMoved',
    x: box.result.value.x,
    y: box.result.value.y,
  })
  await send('Input.dispatchMouseEvent', {
    type: 'mousePressed',
    button: 'left',
    clickCount: 1,
    x: box.result.value.x,
    y: box.result.value.y,
  })
  await send('Input.dispatchMouseEvent', {
    type: 'mouseReleased',
    button: 'left',
    clickCount: 1,
    x: box.result.value.x,
    y: box.result.value.y,
  })

  // Wait 3 seconds
  await new Promise((r) => setTimeout(r, 3000))

  const statusText = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const notice = document.querySelector('[role="status"]');
        const alert = document.querySelector('[role="alert"]');
        return {
          notice: notice ? notice.innerText : null,
          alert: alert ? alert.innerText : null,
          buttonText: document.querySelector('.bg-primary')?.innerText
        };
      })()
    `,
  })
  console.log('DOM status after real click:', statusText.result.value)
  console.log('Request to /api/tts made?', requestMade)

  ws.close()
} finally {
  chrome.kill()
}
