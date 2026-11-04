import { spawn } from 'child_process'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9232',
  '--window-size=1600,900',
  '--disable-gpu',
  'http://127.0.0.1:7860/voice-creation',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9232/json')
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

  // Click "Chạy demo"
  const clickRes = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const demoBtn = btns.find(b => b.textContent.includes('Chạy demo'));
        if (!demoBtn) return { error: 'Demo button not found' };
        demoBtn.click();
        return { success: true, text: demoBtn.textContent };
      })()
    `,
  })
  console.log('Demo click result:', clickRes.result.value)

  // Wait 2.5 seconds into the demo
  await new Promise((r) => setTimeout(r, 2500))

  const progressCheck = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const progressbar = document.querySelector('[role="progressbar"]');
        const logs = Array.from(document.querySelectorAll('[role="log"] li')).map(li => li.innerText);
        const btnText = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Đang chạy'))?.textContent;
        return {
          progressbar: progressbar ? progressbar.getAttribute('aria-valuenow') : null,
          logsCount: logs.length,
          logs,
          btnText
        };
      })()
    `,
  })
  console.log('Demo running after 2.5s:', progressCheck.result.value)

  ws.close()
} finally {
  chrome.kill()
}
