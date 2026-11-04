import { spawn } from 'child_process'
import fs from 'fs'

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const chrome = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9233',
  '--window-size=1600,900',
  '--disable-gpu',
  'http://127.0.0.1:7860/text-to-speech',
])

await new Promise((r) => setTimeout(r, 2500))

try {
  const tabsRes = await fetch('http://127.0.0.1:9233/json')
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
  await send('Page.enable')

  // Paste Vietnamese text
  const pasteRes = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const textarea = document.getElementById('script-input');
        if (!textarea) return { error: 'Textarea not found' };
        
        const testText = "Hôm nay tôi thử nghiệm tính năng tạo giọng đọc tiếng Việt bằng AI từ văn bản dán vào kịch bản.";
        // Simulate paste
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeSetter.call(textarea, testText);
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));

        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return { error: 'Generate button not found', text: textarea.value };

        return { success: true, text: textarea.value, buttonText: genBtn.textContent };
      })()
    `,
  })

  console.log('Paste result:', pasteRes.value)

  // Click "Tạo giọng đọc"
  const clickRes = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const genBtn = btns.find(b => b.textContent.includes('Tạo giọng đọc'));
        if (!genBtn) return { error: 'Button not found' };
        genBtn.click();
        return { success: true, clicked: true };
      })()
    `,
  })

  console.log('Click result:', clickRes.value)

  // Poll for completion (up to 40 seconds)
  let status = null
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 2000))
    const poll = await send('Runtime.evaluate', {
      returnByValue: true,
      expression: `
        (() => {
          const body = document.body.innerText;
          const isGenerating = body.includes('Đang tạo') || body.includes('Đang tổng hợp') || body.includes('Đang nạp');
          const isSuccess = body.includes('Đã tạo giọng thành công') || body.includes('Bản ghi Studio (24 kHz WAV)');
          const noticeEl = document.querySelector('[role="status"]');
          return {
            sec: ${(i + 1) * 2},
            isGenerating,
            isSuccess,
            notice: noticeEl ? noticeEl.textContent.trim() : null
          };
        })()
      `,
    })
    console.log(`[T+${(i + 1) * 2}s]`, poll.value)
    if (poll.value?.notice?.includes('Đã tạo giọng thành công')) {
      status = poll.value
      break
    }
  }

  // Capture screenshot
  const shot = await send('Page.captureScreenshot', { format: 'png' })
  if (shot?.data) {
    fs.writeFileSync('C:\\Users\\jinnr\\.gemini\\antigravity\\brain\\8d36b352-add6-40e0-84f2-30ff15335bbb\\tts_paste_completed.png', Buffer.from(shot.data, 'base64'))
    console.log('Screenshot saved to tts_paste_completed.png')
  }

  ws.close()
} catch (e) {
  console.error('Test error:', e)
} finally {
  chrome.kill()
}
