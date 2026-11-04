import { spawn } from 'child_process'
import fs from 'fs'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9234',
  '--window-size=1600,850',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2000))

try {
  const tabsRes = await fetch('http://127.0.0.1:9234/json')
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

  await send('Page.enable')

  const routes = [
    { url: 'http://127.0.0.1:7860/text-to-speech', name: 'v2_dark_tts.png' },
    { url: 'http://127.0.0.1:7860/voice-changer', name: 'v2_dark_changer.png' },
    { url: 'http://127.0.0.1:7860/voice-creation', name: 'v2_dark_creation.png' },
    { url: 'http://127.0.0.1:7860/voice-library', name: 'v2_dark_library.png' },
  ]

  for (const r of routes) {
    await send('Page.navigate', { url: r.url })
    await new Promise((resolve) => setTimeout(resolve, 1500))
    const shot = await send('Page.captureScreenshot', { format: 'png' })
    if (shot?.data) {
      fs.writeFileSync(`C:\\Users\\jinnr\\.gemini\\antigravity\\brain\\8d36b352-add6-40e0-84f2-30ff15335bbb\\${r.name}`, Buffer.from(shot.data, 'base64'))
      console.log(`Saved ${r.name}`)
    }
  }

  ws.close()
} catch (e) {
  console.error('Error:', e)
} finally {
  chrome.kill()
}
