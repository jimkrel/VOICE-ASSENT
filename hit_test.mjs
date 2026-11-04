import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9229',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9229/json')
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

  await send('Runtime.enable')

  const hitTest = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return { error: 'Not found' };
        const rect = genBtn.getBoundingClientRect();
        const elAtPoint = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
        return {
          btnTag: genBtn.tagName,
          rect,
          elAtPointTag: elAtPoint?.tagName,
          elAtPointClass: elAtPoint?.className,
          isEqual: elAtPoint === genBtn,
          contains: genBtn.contains(elAtPoint)
        };
      })()
    `,
  })
  console.log('Hit test:', hitTest.result.value)

  ws.close()
} finally {
  chrome.kill()
}
