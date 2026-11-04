import asyncio
import json
import base64
import os
import aiohttp

async def run_cdp():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9222/json") as resp:
            tabs = await resp.json()
            ws_url = tabs[0]["webSocketDebuggerUrl"]
            print("Target tab:", ws_url)
        
        async with session.ws_connect(ws_url) as ws:
            msg_id = 1
            async def send_cmd(method, params=None):
                nonlocal msg_id
                cid = msg_id
                msg_id += 1
                await ws.send_json({"id": cid, "method": method, "params": params or {}})
                while True:
                    msg = await ws.receive()
                    data = json.loads(msg.data)
                    if data.get("id") == cid:
                        return data.get("result", {})

            await send_cmd("Page.enable")
            await send_cmd("Runtime.enable")

            async def screenshot(path):
                res = await send_cmd("Page.captureScreenshot", {"format": "png"})
                with open(path, "wb") as f:
                    f.write(base64.b64decode(res["data"]))
                print(f"Saved: {path}")

            # 1. Click "Chạy demo"
            eval_res = await send_cmd("Runtime.evaluate", {
                "expression": """
                (() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Chạy demo'));
                    if (btn) {
                        btn.click();
                        return 'Started demo';
                    }
                    return 'Not found';
                })()
                """
            })
            print("Start:", eval_res.get("result", {}).get("value"))

            # 2. Wait 4.5s -> Mid-flight capture
            await asyncio.sleep(4.5)
            await screenshot(r"E:\VoiceAI\step_running_dark.png")

            # 3. Wait 6.5s -> Complete capture
            await asyncio.sleep(6.5)
            await screenshot(r"E:\VoiceAI\step_complete_dark.png")

            # 4. Click "Chạy lại"
            rerun_res = await send_cmd("Runtime.evaluate", {
                "expression": """
                (() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Chạy lại'));
                    if (btn) {
                        btn.click();
                        return 'Started rerun';
                    }
                    return 'Not found';
                })()
                """
            })
            print("Rerun:", rerun_res.get("result", {}).get("value"))

            # 5. Wait 3s into rerun
            await asyncio.sleep(3.0)
            await screenshot(r"E:\VoiceAI\step_rerun_dark.png")

if __name__ == "__main__":
    asyncio.run(run_cdp())
