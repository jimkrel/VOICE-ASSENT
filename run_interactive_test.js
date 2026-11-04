const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function sendCDP(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 100000);
    const handler = (data) => {
      const msg = JSON.parse(data);
      if (msg.id === id) {
        ws.off('message', handler);
        if (msg.error) reject(msg.error);
        else resolve(msg.result);
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function captureState(ws, outPath) {
  const res = await sendCDP(ws, 'Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(outPath, Buffer.from(res.data, 'base64'));
  console.log(`Saved screenshot to ${outPath}`);
}

async function main() {
  const WebSocket = require('ws');
  const chrome = spawn(chromePath, [
    '--remote-debugging-port=9223',
    '--headless',
    '--disable-gpu',
    '--force-dark-mode',
    '--window-size=1600,817',
    'http://127.0.0.1:7860'
  ]);

  await sleep(2500);

  const tabs = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9223/json', (res) => {
      let b = '';
      res.on('data', c => b += c);
      res.on('end', () => resolve(JSON.parse(b)));
    }).on('error', reject);
  });

  const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  await sendCDP(ws, 'Page.enable');
  await sendCDP(ws, 'Runtime.enable');

  // Verify initial state
  await captureState(ws, 'E:\\VoiceAI\\step1_ready.png');

  // Click "Chạy demo"
  console.log('Triggering click on Chạy demo button...');
  const clickRes = await sendCDP(ws, 'Runtime.evaluate', {
    expression: `
      (() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Chạy demo'));
        if (btn) {
          btn.click();
          return 'Clicked Chạy demo';
        }
        return 'Button not found';
      })()
    `
  });
  console.log('Click result:', clickRes.result.value);

  // Wait 4.5s for mid-run (approx 45% progress)
  await sleep(4500);
  await captureState(ws, 'E:\\VoiceAI\\step2_running.png');

  // Wait 6s more for complete
  await sleep(6500);
  await captureState(ws, 'E:\\VoiceAI\\step3_complete.png');

  // Click "Chạy lại"
  console.log('Triggering click on Chạy lại button...');
  const rerunRes = await sendCDP(ws, 'Runtime.evaluate', {
    expression: `
      (() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Chạy lại'));
        if (btn) {
          btn.click();
          return 'Clicked Chạy lại';
        }
        return 'Rerun button not found';
      })()
    `
  });
  console.log('Rerun click result:', rerunRes.result.value);

  // Wait 3s into re-run
  await sleep(3000);
  await captureState(ws, 'E:\\VoiceAI\\step4_rerun.png');

  ws.close();
  chrome.kill();
  console.log('CDP Test Complete!');
}

main().catch(console.error);
