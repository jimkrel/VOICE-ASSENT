const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function sendCDP(wsUrl, method, params = {}) {
  const WebSocket = require('ws');
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    const id = 1;
    ws.on('open', () => {
      ws.send(JSON.stringify({ id, method, params }));
    });
    ws.on('message', (data) => {
      const res = JSON.parse(data);
      if (res.id === id) {
        ws.close();
        resolve(res.result);
      }
    });
    ws.on('error', reject);
  });
}

async function main() {
  const chrome = spawn(chromePath, [
    '--remote-debugging-port=9222',
    '--headless',
    '--disable-gpu',
    '--window-size=1600,817',
    'http://127.0.0.1:7860'
  ]);
  
  await sleep(2500);

  http.get('http://127.0.0.1:9222/json', (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', async () => {
      const tabs = JSON.parse(body);
      const wsUrl = tabs[0].webSocketDebuggerUrl;
      console.log('Connected to CDP:', wsUrl);
      chrome.kill();
    });
  }).on('error', (e) => {
    console.error('CDP Error:', e);
    chrome.kill();
  });
}
main();
