import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9227',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9227/json')
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
  }

  await send('Runtime.enable')

  const inspectBtn = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return { error: 'Not found' };
        return {
          tagName: genBtn.tagName,
          disabled: genBtn.disabled,
          ariaDisabled: genBtn.getAttribute('aria-disabled'),
          className: genBtn.className,
          innerHTML: genBtn.innerHTML,
          outerHTML: genBtn.outerHTML.slice(0, 200)
        };
      })()
    `,
  })
  console.log('Button details:', inspectBtn.result.value)

  // Try clicking with full MouseEvent dispatch
  const clickTest = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return 'Button not found';
        
        let clicked = false;
        genBtn.addEventListener('click', () => { clicked = true; });
        genBtn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        return { clicked, disabled: genBtn.disabled };
      })()
    `,
  })
  console.log('Click dispatch test:', clickTest.result.value)

  ws.close()
} finally {
  chrome.kill()
}
