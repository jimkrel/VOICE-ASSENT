import re

with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Slider CSS & Controls
slider_css_old = """    .slider-card {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .slider-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
    }
    .slider-badge {
      font-size: 11px;
      font-weight: 600;
      color: var(--text);
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1px 7px;
      font-variant-numeric: tabular-nums;
    }
    .slider-sub-labels {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 500;
      color: var(--text-muted);
    }
    .el-range-input {
      -webkit-appearance: none;
      width: 100%;
      height: 22px;
      background: transparent;
      outline: none;
      margin: 2px 0;
      cursor: pointer;
    }
    .el-range-input::-webkit-slider-runnable-track {
      width: 100%;
      height: 4px;
      background: #e4e4e7;
      border-radius: 999px;
    }
    .el-range-input::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      background: #18181b;
      margin-top: -5.5px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.25);
      transition: transform 0.1s ease;
    }
    .el-range-input::-webkit-slider-thumb:hover {
      transform: scale(1.15);
    }"""

slider_css_new = """    .slider-card {
      display: flex;
      flex-direction: column;
      gap: 2px;
      margin-bottom: 12px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .slider-title {
      font-size: 12.5px;
      font-weight: 600;
      color: #18181b;
    }
    .slider-sub-labels {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      font-size: 10.5px;
      color: #71717a;
      margin-top: 1px;
      margin-bottom: 3px;
    }
    .slider-right-col {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
    }
    .slider-tick-indicator {
      font-size: 8px;
      color: #a1a1aa;
      line-height: 1;
      margin-bottom: 1px;
      font-family: ui-monospace, monospace;
    }
    .el-range-input {
      -webkit-appearance: none;
      width: 100%;
      height: 16px;
      background: transparent;
      outline: none;
      margin: 0;
      cursor: pointer;
    }
    .el-range-input::-webkit-slider-runnable-track {
      width: 100%;
      height: 3px;
      background: linear-gradient(to right, #52525b 0%, #52525b var(--val, 50%), #e4e4e7 var(--val, 50%), #e4e4e7 100%);
      border-radius: 2px;
    }
    .el-range-input::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 3px;
      height: 14px;
      border-radius: 1px;
      background: #18181b;
      margin-top: -5.5px;
      box-shadow: 0 0 2px rgba(0,0,0,0.4);
      transition: background 0.1s ease;
    }
    .el-range-input::-webkit-slider-thumb:hover {
      background: #000000;
    }"""

if slider_css_old in html:
    html = html.replace(slider_css_old, slider_css_new)
    print("Replaced slider CSS successfully")
else:
    print("Could not find exact slider_css_old")

# 2. Update Switches & Language & Format CSS
switch_css_old = """    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 38px;
      height: 22px;
    }
    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .slider-toggle {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #e4e4e7;
      transition: .2s;
      border-radius: 22px;
    }
    .slider-toggle:before {
      position: absolute;
      content: "";
      height: 16px;
      width: 16px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .2s;
      border-radius: 50%;
      box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    input:checked + .slider-toggle {
      background-color: #18181b;
    }
    input:checked + .slider-toggle:before {
      transform: translateX(16px);
    }

    .output-format-badge {
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-secondary);
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      padding: 4px 10px;
    }"""

switch_css_new = """    /* Exact Switch matching Image 1 with outer rectangular border box */
    .toggle-outer-box {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 3px 5px;
      background: #ffffff;
    }
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 36px;
      height: 19px;
    }
    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .slider-toggle {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #f4f4f5;
      border: 1px solid #e4e4e7;
      transition: .2s;
      border-radius: 20px;
    }
    .slider-toggle:before {
      position: absolute;
      content: "";
      height: 13px;
      width: 13px;
      left: 2px;
      bottom: 2px;
      background-color: #d4d4d8;
      transition: .2s;
      border-radius: 50%;
    }
    input:checked + .slider-toggle {
      background-color: #000000;
      border-color: #000000;
    }
    input:checked + .slider-toggle:before {
      background-color: #ffffff;
      transform: translateX(17px);
      box-shadow: 0 1px 3px rgba(0,0,0,0.35);
    }

    /* Exact Language Selector matching Image 1 */
    .el-lang-outer-box {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 3px 6px;
      background: #ffffff;
      cursor: pointer;
    }
    .el-lang-badge {
      background: #2563eb;
      color: #ffffff;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 5px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .el-lang-caret {
      font-size: 9px;
      color: #ffffff;
    }

    /* Exact Format Badge matching Image 1 */
    .output-format-badge {
      font-size: 10.5px;
      font-weight: 500;
      color: #27272a;
      background: #f4f4f5;
      border: none;
      border-radius: 9999px;
      padding: 6px 14px;
      letter-spacing: -0.01em;
    }"""

if switch_css_old in html:
    html = html.replace(switch_css_old, switch_css_new)
    print("Replaced switch & language CSS successfully")
else:
    print("Could not find exact switch_css_old")

with open('E:/VoiceAI/studio_mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)
