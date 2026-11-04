import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9230',
  '--window-size=1600,900',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9230/json')
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

  let ttsRequested = false
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.method === 'Network.requestWillBeSent') {
      if (data.params.request.url.includes('/api/tts')) {
        console.log('>>> API TTS REQUEST DETECTED!', data.params.request.postData)
        ttsRequested = true
      }
    }
  }

  await send('Runtime.enable')
  await send('Network.enable')

  const test = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return { error: 'Button not found' };
        
        // Find React props on the button
        const reactKey = Object.keys(genBtn).find(k => k.startsWith('__reactProps'));
        const props = reactKey ? genBtn[reactKey] : null;
        
        // Directly invoke the onClick handler from React!
        if (props && typeof props.onClick === 'function') {
          props.onClick({ preventDefault: () => {}, stopPropagation: () => {} });
          return { status: 'Invoked props.onClick directly!' };
        }
        
        // Or normal click
        genBtn.click();
        return { status: 'Called genBtn.click()', hasReactProps: !!props };
      })()
    `,
  })
  console.log('Direct test result:', test.result.value)

  // Wait 3 seconds to see if request fires
  await new Promise((r) => setTimeout(r, 3000))
  console.log('Was /api/tts requested?', ttsRequested)

  ws.close()
} finally {
  chrome.kill()
}
