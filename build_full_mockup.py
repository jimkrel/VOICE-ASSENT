import os

def generate_full_mockup():
    html = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thành Âm Studio — Nền tảng Tạo sinh Giọng đọc AI Tiếng Việt & Đa ngôn ngữ</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       1. DESIGN TOKENS (Theo thiet-ke-ui-ux-tieng-viet & ElevenLabs)
       ========================================================================== */
    :root {
      --bg: #faf9f7;
      --surface: #ffffff;
      --surface-subtle: #f8f7f5;
      --surface-hover: #f3f0ff;
      --border: #e8e5e1;
      --border-subtle: #eeece9;
      --border-focus: #b8b0e9;
      --text: #25232a;
      --text-secondary: #514e56;
      --text-muted: #8b8790;
      --accent: #5b4fd0;
      --accent-light: #efedff;
      --accent-hover: #4e42be;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-xl: 18px;
      --radius-pill: 9999px;
      --shadow-sm: 0 1px 3px rgba(37,35,42, 0.05);
      --shadow-md: 0 4px 14px rgba(37,35,42, 0.06);
      --shadow-lg: 0 10px 25px -5px rgba(0,0,0,0.08);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Global Notice */
    .global-announcement {
      background: #18181b;
      color: #fafafa;
      font-size: 11.5px;
      font-weight: 500;
      padding: 6px 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 50;
      flex-shrink: 0;
    }
    .global-announcement b { color: #ffffff; font-weight: 600; }
    .global-close-btn {
      background: transparent;
      border: none;
      color: #a1a1aa;
      cursor: pointer;
      font-size: 13px;
      margin-left: 8px;
    }

    /* App Layout (3-Column Desktop) */
    .app-layout {
      display: flex;
      flex: 1;
      height: calc(100vh - 31px);
      min-height: 0;
      overflow: hidden;
    }

    /* ==========================================================================
       2. WORKSPACE SIDEBAR (Col 1: 210px)
       ========================================================================== */
    .sidebar {
      width: 210px;
      min-width: 210px;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px 12px;
      user-select: none;
      z-index: 30;
    }

    .brand-header {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 4px 8px 16px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .brand-icon {
      width: 32px;
      height: 32px;
      border-radius: var(--radius-md);
      background: #18181b;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .brand-text {
      font-size: 14.5px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #18181b;
    }

    .nav-section-title {
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin: 16px 8px 8px;
    }

    .sidebar-nav {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px;
      border-radius: var(--radius-md);
      color: var(--text-secondary);
      font-size: 12.5px;
      font-weight: 500;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .nav-item:hover {
      background: var(--surface-subtle);
      color: var(--text);
    }
    .nav-item.active {
      background: var(--accent-light);
      color: var(--accent);
      font-weight: 600;
    }
    .nav-item.active svg {
      color: var(--accent);
    }

    .sidebar-bottom {
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-top: 1px solid var(--border-subtle);
      padding-top: 12px;
    }
    .system-card {
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 8px 10px;
      font-size: 10.5px;
    }
    .system-title {
      font-weight: 600;
      color: var(--text);
      display: block;
      margin-bottom: 2px;
    }
    .system-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: #16a34a;
      font-weight: 600;
      font-size: 10px;
    }
    .system-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #16a34a;
      display: inline-block;
    }

    /* ==========================================================================
       3. MAIN WORKSPACE CANVAS (Col 2: Flex-1)
       ========================================================================== */
    .main-workspace {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      height: 100%;
      background: var(--bg);
      overflow: hidden;
    }

    /* Topbar Header */
    .topbar {
      height: 52px;
      min-height: 52px;
      border-bottom: 1px solid var(--border);
      background: var(--surface);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 20;
    }
    .breadcrumb {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      color: #18181b;
    }
    .crumb-sub {
      color: var(--text-muted);
      font-weight: 500;
    }
    .topbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .search-pill {
      display: flex;
      align-items: center;
      gap: 7px;
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      padding: 5px 14px;
      font-size: 11.5px;
      color: var(--text-muted);
      cursor: text;
    }
    .topbar-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      color: #15803d;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
    }

    /* Canvas Body */
    .workspace-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .screen-container {
      width: 100%;
      max-width: 920px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .screen-header h2 {
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.03em;
      color: #18181b;
    }
    .screen-header p {
      margin-top: 3px;
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.5;
    }

    /* 3.1. MODULE 1: TEXT TO SPEECH */
    .emotion-toolbar {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 8px 12px;
      box-shadow: var(--shadow-sm);
    }
    .emotion-title {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text);
      white-space: nowrap;
      padding-right: 6px;
      border-right: 1px solid var(--border-subtle);
    }
    .emotion-pills {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .emotion-pills::-webkit-scrollbar { display: none; }
    .emotion-pill-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #fcfbfa;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 5px 10px;
      font-size: 11px;
      font-weight: 500;
      color: var(--text-secondary);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.12s ease;
    }
    .emotion-pill-btn:hover {
      background: var(--accent-light);
      border-color: #d4cef0;
      color: var(--accent);
      transform: translateY(-1px);
    }

    /* Textarea Box */
    .editor-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .editor-card:focus-within {
      border-color: #beb6e9;
      box-shadow: 0 0 0 3px #efedff;
    }
    .editor-textarea {
      width: 100%;
      min-height: 240px;
      border: none;
      outline: none;
      resize: vertical;
      padding: 18px 20px;
      font-size: 13.5px;
      line-height: 1.65;
      color: var(--text);
      background: transparent;
      font-family: inherit;
    }
    .editor-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-subtle);
      padding: 10px 18px;
      background: #ffffff;
    }
    .char-counter {
      font-size: 11px;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
    }
    .editor-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-ghost {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 11.5px;
      font-weight: 500;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: background 0.12s ease;
    }
    .btn-ghost:hover { background: var(--surface-subtle); }
    .btn-primary {
      background: #18181b;
      color: #ffffff;
      border: none;
      border-radius: var(--radius-md);
      padding: 8px 18px;
      font-size: 12px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
      transition: background 0.15s ease, transform 0.1s ease;
    }
    .btn-primary:hover { background: #000000; transform: translateY(-1px); }

    /* Output Dock & Audio Player */
    .output-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      padding: 16px 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .status-shimmer-pill {
      background: #fcfbfa;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      position: relative;
    }
    .status-pill-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
    }
    .status-left {
      display: flex;
      align-items: center;
      gap: 7px;
      font-weight: 600;
      color: #18181b;
    }
    .status-indicator-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #16a34a;
      box-shadow: 0 0 6px rgba(22,163,74,0.6);
    }
    .status-tags {
      display: inline-flex;
      gap: 5px;
      font-weight: 500;
      color: var(--text-secondary);
      font-size: 11px;
    }
    .tag-badge {
      background: #ede9fe;
      color: #5b21b6;
      border-radius: 4px;
      padding: 1px 6px;
      font-size: 10px;
      font-weight: 600;
    }
    .status-dismiss-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .countdown-chip {
      background: #e4e4e7;
      color: #27272a;
      font-size: 10px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
    }
    .status-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 13px;
    }
    .status-progress-track {
      width: 100%;
      height: 4px;
      background: #f4f4f5;
      border-radius: 2px;
      overflow: hidden;
    }
    .status-progress-bar {
      height: 100%;
      width: 100%;
      background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
      background-size: 200% 100%;
      animation: shimmer 2s infinite linear;
    }
    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }
    audio {
      width: 100%;
      height: 38px;
      outline: none;
      border-radius: 8px;
    }

    /* 3.2. MODULE 2: VOICE CREATION */
    .tab-nav-bar {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }
    .tab-pill {
      background: transparent;
      border: none;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: var(--radius-md);
      transition: all 0.12s ease;
    }
    .tab-pill.active {
      background: var(--surface);
      color: #18181b;
      box-shadow: var(--shadow-sm);
    }

    .dropzone-box {
      border: 2px dashed #dcd8d2;
      background: #faf9f7;
      border-radius: var(--radius-xl);
      padding: 32px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .dropzone-box:hover {
      border-color: #8176d7;
      background: #f3f0ff;
    }
    .dropzone-icon {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-lg);
      background: #efedff;
      color: #675bd0;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
    }
    .dropzone-title {
      font-size: 13.5px;
      font-weight: 600;
      color: #18181b;
    }
    .dropzone-sub {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .input-field-wrap {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 14px;
    }
    .input-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text);
    }
    .clean-input {
      width: 100%;
      height: 40px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--surface);
      padding: 0 14px;
      font-size: 12.5px;
      color: var(--text);
      outline: none;
      transition: border-color 0.15s ease;
    }
    .clean-input:focus {
      border-color: #b8b0e9;
      box-shadow: 0 0 0 3px #efedff;
    }

    /* 3.3. MODULE 3: VOICE CHANGER */
    .changer-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }
    .changer-target-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* 3.4. MODULE 4: VOICE LIBRARY */
    .vlib-filter-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 6px;
    }
    .vlib-pill {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      padding: 5px 14px;
      font-size: 11px;
      font-weight: 500;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .vlib-pill:hover {
      background: var(--surface-hover);
      color: var(--accent);
    }
    .vlib-pill.active {
      background: #18181b;
      border-color: #18181b;
      color: #ffffff;
      font-weight: 600;
    }

    .vlib-grid {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .vlib-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      transition: all 0.15s ease;
    }
    .vlib-card:hover {
      border-color: #beb6e9;
      box-shadow: var(--shadow-sm);
    }
    .vlib-card.selected {
      border-color: #a89bf5;
      background: #fcfbff;
    }
    .vlib-left {
      display: flex;
      align-items: center;
      gap: 14px;
      min-width: 0;
      flex: 1;
    }
    .vlib-meta {
      min-width: 0;
      flex: 1;
    }
    .vlib-name-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .vlib-name {
      font-size: 13px;
      font-weight: 600;
      color: #18181b;
    }
    .vlib-tag {
      background: #f4f2ef;
      color: #77737c;
      font-size: 10px;
      font-weight: 500;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
    }
    .vlib-tags-sub {
      font-size: 11px;
      color: var(--text-secondary);
      margin-top: 2px;
    }
    .vlib-quote {
      font-size: 11px;
      color: var(--text-muted);
      font-style: italic;
      margin-top: 2px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .vlib-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .vlib-play-circle-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: #18181b;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .vlib-play-circle-btn:hover {
      background: #18181b;
      color: #ffffff;
    }
    .vlib-use-btn {
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 6px 14px;
      font-size: 11px;
      font-weight: 600;
      color: #18181b;
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .vlib-use-btn:hover {
      background: #18181b;
      color: #ffffff;
    }

    /* 5 Radial Gradient Voice Orbs (Thực tế Next.js) */
    .voice-orb {
      width: 40px;
      height: 40px;
      min-width: 40px;
      border-radius: 50%;
      border: 1px solid rgba(255,255,255,0.7);
      box-shadow: 0 2px 8px rgba(35,69,120,0.18);
    }
    .voice-orb.tone-aqua { background: radial-gradient(circle at 30% 25%, #e3ffff 0%, #64d8ec 28%, #3b83ee 62%, #8755dc 100%); }
    .voice-orb.tone-blue { background: radial-gradient(circle at 30% 25%, #d8f7ff 0%, #52c0e9 32%, #2575c8 68%, #183b78 100%); }
    .voice-orb.tone-violet { background: radial-gradient(circle at 30% 25%, #f3dcff 0%, #b772e2 30%, #5147cc 68%, #312a63 100%); }
    .voice-orb.tone-coral { background: radial-gradient(circle at 30% 25%, #fff1df 0%, #ff9c70 30%, #df5d74 64%, #684cb9 100%); }
    .voice-orb.tone-green { background: radial-gradient(circle at 30% 25%, #e7fff2 0%, #76d9b0 30%, #398db5 66%, #566fda 100%); }

    /* ==========================================================================
       4. WORKSPACE SETTINGS PANEL (Col 3: 290px - Image 1 & 2 Standard)
       ========================================================================== */
    .inspector {
      width: 290px;
      min-width: 290px;
      background: var(--surface);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow-y: auto;
      z-index: 20;
    }
    .inspector-tabs {
      display: flex;
      border-bottom: 1px solid var(--border-subtle);
      padding: 0 16px;
      gap: 16px;
    }
    .inspector-tab {
      padding: 12px 2px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      position: relative;
    }
    .inspector-tab.active {
      color: #18181b;
      font-weight: 600;
    }
    .inspector-tab.active::after {
      content: "";
      position: absolute;
      bottom: -1px;
      left: 0;
      right: 0;
      height: 2px;
      background: #18181b;
    }
    .inspector-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* Voice Picker Pill */
    .inspector-voice-card {
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 10px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
    }
    .inspector-voice-info {
      min-width: 0;
      flex: 1;
    }
    .inspector-voice-title {
      font-size: 11.5px;
      font-weight: 600;
      color: #18181b;
    }
    .inspector-voice-desc {
      font-size: 10.5px;
      color: var(--text-muted);
      margin-top: 1px;
    }

    /* 4 Sliders Matching Image 1 */
    .slider-card {
      display: flex;
      flex-direction: column;
      gap: 2px;
      margin-bottom: 4px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .slider-title {
      font-size: 12px;
      font-weight: 600;
      color: #18181b;
    }
    .slider-sub-labels {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      font-size: 10px;
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
    }

    /* Accordion Tùy Chỉnh Nâng Cao */
    details.advanced-details {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--surface);
      padding: 10px 12px;
      transition: all 0.2s ease;
    }
    details.advanced-details summary {
      font-size: 12px;
      font-weight: 600;
      color: #18181b;
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    details.advanced-details summary::-webkit-details-marker { display: none; }
    .advanced-content {
      margin-top: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    /* Audio Effects (Image 2) */
    .el-fx-section {
      border-top: 1px solid var(--border-subtle);
      padding-top: 10px;
    }
    .el-fx-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      margin-bottom: 8px;
    }
    .el-fx-title {
      font-size: 11.5px;
      font-weight: 600;
      color: #18181b;
    }
    .el-fx-row {
      position: relative;
      display: flex;
      align-items: center;
      height: 36px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      margin-bottom: 6px;
    }
    .el-fx-label-cell {
      display: flex;
      align-items: center;
      gap: 6px;
      width: 95px;
      min-width: 95px;
      height: 100%;
      padding: 0 10px;
      border-right: 1px solid var(--border);
      color: var(--text-secondary);
      font-size: 11.5px;
    }
    .el-fx-select-cell {
      flex: 1;
      height: 100%;
      padding: 0 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
      font-weight: 500;
      color: #18181b;
      cursor: pointer;
    }
    .el-fx-remove-cell {
      width: 32px;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      cursor: pointer;
    }
    .el-fx-remove-cell:hover { color: #dc2626; }

    /* Popover */
    .el-fx-popover {
      display: none;
      position: absolute;
      top: 40px;
      left: 70px;
      right: 0;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      padding: 4px;
      z-index: 100;
    }
    .el-fx-popover.open { display: block; }
    .el-fx-opt {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 10px;
      font-size: 11.5px;
      color: #18181b;
      cursor: pointer;
      border-radius: 4px;
    }
    .el-fx-opt:hover { background: var(--surface-subtle); }
    .el-fx-opt .fx-check { display: none; color: #18181b; }
    .el-fx-opt.active .fx-check { display: block; }

    /* Toggles & Language (Image 1) */
    .control-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      min-height: 32px;
    }
    .control-row-label {
      font-size: 11px;
      font-weight: 500;
      color: #3f3f46;
      white-space: nowrap;
    }
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
    .output-format-badge {
      font-size: 10px;
      font-weight: 500;
      color: #27272a;
      background: #f4f4f5;
      border-radius: var(--radius-pill);
      padding: 5px 10px;
      white-space: nowrap;
    }
    .btn-reset {
      background: transparent;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 6px 12px;
      color: var(--text-secondary);
      font-size: 11px;
      font-weight: 500;
      cursor: pointer;
      margin-top: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }
    .btn-reset:hover { background: var(--surface-subtle); }
  </style>
</head>
<body>

  <!-- Top Announcement Bar -->
  <div class="global-announcement">
    <span>✨ <b>Thành Âm Studio V2.0</b> — Kiến trúc AI mới tạo sinh giọng nói đa sắc thái thời gian thực trên GPU GTX 1650</span>
    <button class="global-close-btn" onclick="this.parentElement.style.display='none'">✕</button>
  </div>

  <div class="app-layout">
    
    <!-- 1. SIDEBAR -->
    <aside class="sidebar">
      <div>
        <div class="brand-header">
          <div class="brand-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v3"/></svg>
          </div>
          <span class="brand-text">Thành Âm</span>
        </div>

        <div class="nav-section-title">Không gian làm việc</div>
        <nav class="sidebar-nav">
          <a class="nav-item active" id="nav-tts" onclick="switchTool('tts')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="6 3 20 12 6 21 6 3"/></svg>
            <span>Đọc kịch bản</span>
          </a>
          <a class="nav-item" id="nav-vc" onclick="switchTool('vc')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg>
            <span>Tạo giọng mới</span>
          </a>
          <a class="nav-item" id="nav-changer" onclick="switchTool('changer')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg>
            <span>Đổi giọng</span>
          </a>
          <a class="nav-item" id="nav-lib" onclick="switchTool('lib')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
            <span>Kho giọng đọc</span>
          </a>
        </nav>
      </div>

      <div class="sidebar-bottom">
        <div class="system-card">
          <span class="system-title">NVIDIA GTX 1650 • 4 GB</span>
          <span class="system-pill"><span class="system-dot"></span> CUDA FP16 Trực tuyến</span>
        </div>
        <div class="system-card">
          <span class="system-title">Mạng nội bộ LAN</span>
          <span style="color:#71717a; font-size:10px;">http://192.168.1.8:7860</span>
        </div>
      </div>
    </aside>

    <!-- 2. MAIN WORKSPACE -->
    <main class="main-workspace">
      
      <!-- TopBar -->
      <div class="topbar">
        <div class="breadcrumb">
          <span>Thành Âm</span>
          <span class="crumb-sub" id="crumb-tool">/ Đọc kịch bản (Text to Speech)</span>
        </div>
        <div class="topbar-right">
          <div class="search-pill">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <span>Tìm kiếm giọng đọc, kịch bản...</span>
          </div>
          <span class="topbar-badge">● GTX 1650 FP16</span>
        </div>
      </div>

      <!-- Workspace Body -->
      <div class="workspace-body">
        <div class="screen-container">

          <!-- ================= MODULE 1: TTS ================= -->
          <div id="ws-tts" style="display: flex; flex-direction: column; gap: 16px;">
            <div class="screen-header">
              <h2>Biến kịch bản thành giọng đọc</h2>
              <p>Dán nội dung, thêm sắc thái cho từng câu và chọn giọng đọc ở bảng cài đặt.</p>
            </div>

            <!-- Emotion Toolbar (Lucide Icons) -->
            <div class="emotion-toolbar">
              <div class="emotion-title">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7165cc" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
                <span>Sắc thái</span>
              </div>
              <div class="emotion-pills">
                <button class="emotion-pill-btn" onclick="insertTag('[kịch tính]')">🎭 Kịch tính</button>
                <button class="emotion-pill-btn" onclick="insertTag('[thì thầm]')">🤫 Thì thầm</button>
                <button class="emotion-pill-btn" onclick="insertTag('[hào hứng]')">🔥 Hào hứng</button>
                <button class="emotion-pill-btn" onclick="insertTag('[buồn]')">🌧️ Buồn bã</button>
                <button class="emotion-pill-btn" onclick="insertTag('[tức giận]')">⚡ Tức giận</button>
                <button class="emotion-pill-btn" onclick="insertTag('[thở dài]')">💨 Thở dài</button>
                <button class="emotion-pill-btn" onclick="insertTag('[điềm tĩnh]')">🍃 Điềm tĩnh</button>
              </div>
            </div>

            <!-- Editor Card -->
            <div class="editor-card">
              <textarea class="editor-textarea" id="script-input" maxlength="5000" oninput="updateCount()">[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.
[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.
[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số trên GPU GTX 1650.
[điềm tĩnh] Cảm ơn bạn đã lắng nghe.</textarea>
              <div class="editor-footer">
                <span class="char-counter" id="char-count">364 / 5.000 ký tự</span>
                <div class="editor-actions">
                  <button class="btn-ghost" onclick="clearScript()">Xóa</button>
                  <button class="btn-ghost" onclick="restoreSampleScript()">Mẫu</button>
                  <button class="btn-primary" onclick="triggerGenerate()">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
                    <span>Tạo giọng nói</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Output Dock -->
            <div class="output-card" id="output-dock">
              <div class="status-shimmer-pill">
                <div class="status-pill-head">
                  <div class="status-left">
                    <span class="status-indicator-dot"></span>
                    <span id="status-title">Đã tạo giọng nói thành công</span>
                    <div class="status-tags">
                      <span>⏱️ 11.8s</span>
                      <span>• 17.5s âm thanh</span>
                      <span class="tag-badge">dramatic</span>
                      <span class="tag-badge">whisper</span>
                    </div>
                  </div>
                  <div class="status-dismiss-wrap">
                    <span class="countdown-chip" id="countdown-chip">10s</span>
                    <button class="status-close-btn" onclick="dismissDock()">✕</button>
                  </div>
                </div>
                <div class="status-progress-track">
                  <div class="status-progress-bar"></div>
                </div>
              </div>
              <audio controls id="audio-player">
                <source src="" type="audio/wav">
              </audio>
            </div>
          </div>

          <!-- ================= MODULE 2: VOICE CREATION ================= -->
          <div id="ws-vc" style="display: none; flex-direction: column; gap: 16px;">
            <div class="screen-header">
              <h2>Tạo giọng đọc mới</h2>
              <p>Nhân bản giọng từ tệp âm thanh mẫu hoặc thiết kế đặc tính giọng đọc theo ý bạn.</p>
            </div>

            <div class="tab-nav-bar">
              <button class="tab-pill active" id="vc-tab-clone" onclick="switchVcTab('clone')">Nhân bản giọng (Voice Clone)</button>
              <button class="tab-pill" id="vc-tab-design" onclick="switchVcTab('design')">Thiết kế giọng (Voice Design)</button>
            </div>

            <!-- Clone Tab -->
            <div id="vc-pane-clone" style="display: flex; flex-direction: column; gap: 14px;">
              <div class="dropzone-box" onclick="alert('Mở hộp thoại chọn tệp âm thanh mẫu (WAV, MP3 <= 50MB)')">
                <div class="dropzone-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                </div>
                <span class="dropzone-title">Kéo thả tệp âm thanh mẫu vào đây</span>
                <span class="dropzone-sub">hoặc nhấn để duyệt tệp • Hỗ trợ MP3, WAV, M4A (Khuyến nghị 5–15 giây)</span>
              </div>
              <div class="input-field-wrap">
                <label class="input-label">Tên giọng đọc mới</label>
                <input class="clean-input" placeholder="Ví dụ: Giọng MC Minh Quân">
              </div>
              <button class="btn-primary" style="align-self: flex-start; margin-top: 6px;" onclick="alert('Đang trích xuất đặc trưng âm học và lưu vào Kho giọng đọc!')">
                <span>Tạo và lưu giọng đọc</span>
              </button>
            </div>

            <!-- Design Tab -->
            <div id="vc-pane-design" style="display: none; flex-direction: column; gap: 14px;">
              <div class="input-field-wrap">
                <label class="input-label">Mô tả phong cách giọng mong muốn</label>
                <input class="clean-input" placeholder="Ví dụ: Giọng nữ trẻ trung, sôi nổi, phong cách podcast công nghệ">
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 8px;">
                <div class="slider-card">
                  <span class="slider-title">Độ tuổi</span>
                  <div class="slider-sub-labels"><span>Trẻ</span><span>Lớn tuổi</span></div>
                  <input type="range" class="el-range-input" value="30">
                </div>
                <div class="slider-card">
                  <span class="slider-title">Cao độ (Pitch)</span>
                  <div class="slider-sub-labels"><span>Trầm</span><span>Bổng</span></div>
                  <input type="range" class="el-range-input" value="50">
                </div>
              </div>
              <button class="btn-primary" style="align-self: flex-start; margin-top: 6px;" onclick="alert('Đang tổng hợp mẫu thiết kế giọng!')">
                <span>Tạo thử giọng thiết kế</span>
              </button>
            </div>
          </div>

          <!-- ================= MODULE 3: VOICE CHANGER ================= -->
          <div id="ws-changer" style="display: none; flex-direction: column; gap: 16px;">
            <div class="screen-header">
              <h2>Đổi giọng nói (Voice Changer)</h2>
              <p>Tải tệp âm thanh nguồn lên và chuyển đổi sang giọng đích đã chọn ở bảng cài đặt.</p>
            </div>

            <div class="dropzone-box" onclick="alert('Mở hộp thoại chọn tệp cần đổi giọng (Audio/Video <= 50MB)')">
              <div class="dropzone-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg>
              </div>
              <span class="dropzone-title">Kéo thả tệp âm thanh / video cần đổi giọng</span>
              <span class="dropzone-sub">MP3, WAV, M4A, MP4 • Tối đa 50 MB</span>
            </div>

            <div class="changer-target-card">
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="voice-orb tone-aqua" id="changer-target-orb"></div>
                <div>
                  <span style="font-size: 11px; color: var(--text-muted); display: block;">Giọng đích được áp dụng:</span>
                  <span style="font-size: 13px; font-weight: 600; color: #18181b;" id="changer-target-name">Hope — upbeat and clear (US Nữ)</span>
                </div>
              </div>
              <button class="btn-ghost" onclick="switchTool('lib')">Đổi giọng khác</button>
            </div>

            <button class="btn-primary" style="align-self: flex-start; margin-top: 6px;" onclick="alert('Đang thực hiện chuyển đổi giọng nói qua DiT trên GPU GTX 1650!')">
              <span>Bắt đầu đổi giọng</span>
            </button>
          </div>

          <!-- ================= MODULE 4: VOICE LIBRARY ================= -->
          <div id="ws-lib" style="display: none; flex-direction: column; gap: 16px;">
            <div class="screen-header">
              <h2>Kho giọng đọc</h2>
              <p>Khám phá các chất giọng tự nhiên, chọn nghe thử và áp dụng trực tiếp cho dự án của bạn.</p>
            </div>

            <!-- Filter Pills -->
            <div class="vlib-filter-bar">
              <button class="vlib-pill active" onclick="filterVoices('all', this)">Tất cả</button>
              <button class="vlib-pill" onclick="filterVoices('US English', this)">US English</button>
              <button class="vlib-pill" onclick="filterVoices('UK English', this)">UK English</button>
              <button class="vlib-pill" onclick="filterVoices('Nam', this)">Nam</button>
              <button class="vlib-pill" onclick="filterVoices('Nữ', this)">Nữ</button>
              <button class="vlib-pill" onclick="filterVoices('Tiếng Việt', this)">Tiếng Việt</button>
              <button class="vlib-pill" onclick="filterVoices('Giọng tự tạo', this)">Giọng tự tạo</button>
            </div>

            <!-- Voice Grid Cards -->
            <div class="vlib-grid" id="vlib-grid">
              
              <!-- 1. Hope -->
              <div class="vlib-card" data-tags="US English Nữ" data-voice="hope">
                <div class="vlib-left">
                  <div class="voice-orb tone-aqua"></div>
                  <div class="vlib-meta">
                    <div class="vlib-name-row">
                      <span class="vlib-name">Hope — upbeat and clear</span>
                      <span class="vlib-tag">ElevenLabs Original</span>
                    </div>
                    <div class="vlib-tags-sub">English (US) • Nữ • Trong trẻo, tươi sáng</div>
                    <div class="vlib-quote">“Deep inside the Black Forest, investigators discovered an abandoned radio tower.”</div>
                  </div>
                </div>
                <div class="vlib-actions">
                  <button class="vlib-play-circle-btn" onclick="alert('Đang phát giọng đọc mẫu: Hope')">▶</button>
                  <button class="vlib-use-btn" onclick="useVoice('hope', 'Hope — upbeat and clear', 'tone-aqua', 'Trong trẻo, tươi sáng')">Dùng giọng này</button>
                </div>
              </div>

              <!-- 2. Marcus -->
              <div class="vlib-card" data-tags="US English Nam" data-voice="marcus">
                <div class="vlib-left">
                  <div class="voice-orb tone-blue"></div>
                  <div class="vlib-meta">
                    <div class="vlib-name-row">
                      <span class="vlib-name">Marcus — documentary and crime</span>
                      <span class="vlib-tag">Hệ thống</span>
                    </div>
                    <div class="vlib-tags-sub">English (US) • Nam • Trầm, rõ nét, phù hợp tài liệu</div>
                    <div class="vlib-quote">“The year was 1994. A signal appeared from a station no one had used in decades.”</div>
                  </div>
                </div>
                <div class="vlib-actions">
                  <button class="vlib-play-circle-btn" onclick="alert('Đang phát giọng đọc mẫu: Marcus')">▶</button>
                  <button class="vlib-use-btn" onclick="useVoice('marcus', 'Marcus — documentary and crime', 'tone-blue', 'Trầm, rõ nét, phù hợp tài liệu')">Dùng giọng này</button>
                </div>
              </div>

              <!-- 3. Liam -->
              <div class="vlib-card" data-tags="UK English Nam" data-voice="liam">
                <div class="vlib-left">
                  <div class="voice-orb tone-violet"></div>
                  <div class="vlib-meta">
                    <div class="vlib-name-row">
                      <span class="vlib-name">Liam — storyteller and essay</span>
                      <span class="vlib-tag">Hệ thống</span>
                    </div>
                    <div class="vlib-tags-sub">English (UK) • Nam • Ấm áp, gần gũi, nhịp kể tự nhiên</div>
                    <div class="vlib-quote">“Have you ever wondered why some stories stay with you forever?”</div>
                  </div>
                </div>
                <div class="vlib-actions">
                  <button class="vlib-play-circle-btn" onclick="alert('Đang phát giọng đọc mẫu: Liam')">▶</button>
                  <button class="vlib-use-btn" onclick="useVoice('liam', 'Liam — storyteller and essay', 'tone-violet', 'Ấm áp, gần gũi, nhịp kể tự nhiên')">Dùng giọng này</button>
                </div>
              </div>

              <!-- 4. Alex -->
              <div class="vlib-card" data-tags="US English Nam" data-voice="alex">
                <div class="vlib-left">
                  <div class="voice-orb tone-coral"></div>
                  <div class="vlib-meta">
                    <div class="vlib-name-row">
                      <span class="vlib-name">Alex — movie recap and shorts</span>
                      <span class="vlib-tag">Hệ thống</span>
                    </div>
                    <div class="vlib-tags-sub">English (US) • Nam • Năng lượng, nhịp nhanh, video ngắn</div>
                    <div class="vlib-quote">“In a city that never sleeps, one message changed everything.”</div>
                  </div>
                </div>
                <div class="vlib-actions">
                  <button class="vlib-play-circle-btn" onclick="alert('Đang phát giọng đọc mẫu: Alex')">▶</button>
                  <button class="vlib-use-btn" onclick="useVoice('alex', 'Alex — movie recap and shorts', 'tone-coral', 'Năng lượng, nhịp nhanh, video ngắn')">Dùng giọng này</button>
                </div>
              </div>

              <!-- 5. Minh Anh -->
              <div class="vlib-card" data-tags="Tiếng Việt Nữ" data-voice="minh-anh">
                <div class="vlib-left">
                  <div class="voice-orb tone-green"></div>
                  <div class="vlib-meta">
                    <div class="vlib-name-row">
                      <span class="vlib-name">Minh Anh — ấm áp và rõ ràng</span>
                      <span class="vlib-tag">Hệ thống</span>
                    </div>
                    <div class="vlib-tags-sub">Tiếng Việt • Nữ • Giọng nữ miền Bắc, nhẹ nhàng và tự nhiên</div>
                    <div class="vlib-quote">“Xin chào, mời bạn cùng khám phá câu chuyện thú vị hôm nay.”</div>
                  </div>
                </div>
                <div class="vlib-actions">
                  <button class="vlib-play-circle-btn" onclick="alert('Đang phát giọng đọc mẫu: Minh Anh')">▶</button>
                  <button class="vlib-use-btn" onclick="useVoice('minh-anh', 'Minh Anh — ấm áp và rõ ràng', 'tone-green', 'Giọng nữ Bắc nhẹ nhàng')">Dùng giọng này</button>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- 3. WORKSPACE SETTINGS PANEL (INSPECTOR) -->
    <aside class="inspector" id="inspector">
      <div class="inspector-tabs">
        <div class="inspector-tab active">Cài đặt</div>
        <div class="inspector-tab" onclick="alert('Lịch sử các bản thu đã tạo')">Lịch sử</div>
      </div>

      <div class="inspector-body">
        
        <!-- Voice Card Pill -->
        <div class="slider-title" style="margin-bottom: -8px;">Giọng đọc</div>
        <div class="inspector-voice-card" onclick="switchTool('lib')">
          <div class="voice-orb tone-aqua" id="inspector-orb"></div>
          <div class="inspector-voice-info">
            <span class="inspector-voice-title" id="inspector-name">Hope — upbeat and clear</span>
            <span class="inspector-voice-desc" id="inspector-desc">US Nữ • Trong trẻo, tươi sáng</span>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>

        <!-- 1. Tốc độ đọc (Image 1 Standard) -->
        <div class="slider-card">
          <div class="slider-header">
            <span class="slider-title">Tốc độ đọc</span>
          </div>
          <div class="slider-sub-labels">
            <span>Chậm hơn</span>
            <div class="slider-right-col">
              <span class="slider-tick-indicator">v</span>
              <span>Nhanh hơn</span>
            </div>
          </div>
          <input type="range" class="el-range-input" min="0.70" max="1.40" step="0.05" value="0.95" style="--val: 35.7%;" oninput="const p = ((this.value - 0.70)/0.70)*100; this.style.setProperty('--val', p + '%');">
        </div>

        <!-- Accordion Tùy Chỉnh Nâng Cao -->
        <details class="advanced-details" open>
          <summary>
            <span>Tùy chỉnh nâng cao</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </summary>
          <div class="advanced-content">
            
            <!-- 2. Độ ổn định -->
            <div class="slider-card">
              <div class="slider-header"><span class="slider-title">Độ ổn định</span></div>
              <div class="slider-sub-labels">
                <span>Linh hoạt, cảm xúc</span>
                <div class="slider-right-col"><span class="slider-tick-indicator">v</span><span>Ổn định, đều đặn</span></div>
              </div>
              <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.45" style="--val: 45%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
            </div>

            <!-- 3. Độ bám giọng mẫu -->
            <div class="slider-card">
              <div class="slider-header"><span class="slider-title">Độ bám giọng mẫu</span></div>
              <div class="slider-sub-labels">
                <span>Linh hoạt</span>
                <div class="slider-right-col"><span class="slider-tick-indicator">v</span><span>Rất giống mẫu</span></div>
              </div>
              <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.75" style="--val: 75%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
            </div>

            <!-- 4. Nhấn nhá cảm xúc -->
            <div class="slider-card">
              <div class="slider-header"><span class="slider-title">Nhấn nhá cảm xúc</span></div>
              <div class="slider-sub-labels">
                <span>Tự nhiên</span>
                <div class="slider-right-col"><span class="slider-tick-indicator">v</span><span>Kịch tính</span></div>
              </div>
              <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.05" style="--val: 5%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
            </div>

            <!-- Audio effects (Image 2 Standard) -->
            <div class="el-fx-section">
              <div class="el-fx-header">
                <span class="el-fx-title">Audio effects</span>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
              <div class="el-fx-row" id="fx-row-dist">
                <div class="el-fx-label-cell">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="11" r="2.5"/><path d="M12 13.5v4.5"/><path d="M9.5 18h5"/><path d="M6.5 7.5a7.5 7.5 0 0 0 0 7" stroke-dasharray="2 2"/><path d="M17.5 7.5a7.5 7.5 0 0 1 0 7" stroke-dasharray="2 2"/></svg>
                  <span>Distance</span>
                </div>
                <div class="el-fx-select-cell" onclick="togglePopover('menu-dist')">
                  <span id="txt-dist">Far</span>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"/></svg>
                </div>
                <div class="el-fx-remove-cell" onclick="document.getElementById('fx-row-dist').style.display='none'">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                </div>
                <!-- Popover -->
                <div class="el-fx-popover" id="menu-dist">
                  <div class="el-fx-opt" onclick="setFx('txt-dist', 'Near', this)"><span>Near</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                  <div class="el-fx-opt" onclick="setFx('txt-dist', 'Medium', this)"><span>Medium</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                  <div class="el-fx-opt active" onclick="setFx('txt-dist', 'Far', this)"><span>Far</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                </div>
              </div>

              <!-- Space Row -->
              <div class="el-fx-row" id="fx-row-space">
                <div class="el-fx-label-cell">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v3"/></svg>
                  <span>Space</span>
                </div>
                <div class="el-fx-select-cell" onclick="togglePopover('menu-space')">
                  <span id="txt-space">Studio (Dry)</span>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                </div>
                <div class="el-fx-remove-cell" onclick="document.getElementById('fx-row-space').style.display='none'">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                </div>
                <!-- Popover -->
                <div class="el-fx-popover" id="menu-space">
                  <div class="el-fx-opt active" onclick="setFx('txt-space', 'Studio (Dry)', this)"><span>Studio (Dry)</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                  <div class="el-fx-opt" onclick="setFx('txt-space', 'Small Room', this)"><span>Small Room</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                  <div class="el-fx-opt" onclick="setFx('txt-space', 'Large Hall', this)"><span>Large Hall</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                  <div class="el-fx-opt" onclick="setFx('txt-space', 'Phone Line', this)"><span>Phone Line</span><svg class="fx-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                </div>
              </div>
            </div>

            <!-- Language Row (Image 1) -->
            <div class="control-row">
              <span class="control-row-label">Ngôn ngữ</span>
              <div class="el-lang-outer-box" onclick="alert('Ngôn ngữ: English / Tiếng Việt')">
                <span class="el-lang-badge">English <span style="font-size: 8px;">▼</span></span>
              </div>
            </div>

            <!-- Master Switch (Image 1) -->
            <div class="control-row">
              <span class="control-row-label">Master chuẩn phòng thu (-14 LUFS)</span>
              <div class="toggle-outer-box">
                <label class="toggle-switch">
                  <input type="checkbox" checked>
                  <span class="slider-toggle"></span>
                </label>
              </div>
            </div>

            <!-- Denoise Switch (Image 1) -->
            <div class="control-row">
              <span class="control-row-label">Loại bỏ tiếng ồn nền</span>
              <div class="toggle-outer-box">
                <label class="toggle-switch">
                  <input type="checkbox">
                  <span class="slider-toggle"></span>
                </label>
              </div>
            </div>

            <!-- Format Pill (Image 1) -->
            <div class="control-row">
              <span class="control-row-label">Định dạng đầu ra</span>
              <span class="output-format-badge">WAV · 24 kHz · TruePeak -1.0dB</span>
            </div>

            <button class="btn-reset" onclick="alert('Đã khôi phục cài đặt gốc!')">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              Đặt lại cài đặt
            </button>

          </div>
        </details>

      </div>
    </aside>

  </div>

  <!-- INTERACTIVE SCRIPTS (Full State Management) -->
  <script>
    const TOOL_TITLES = {
      'tts': '/ Đọc kịch bản (Text to Speech)',
      'vc': '/ Tạo giọng mới (Voice Creation)',
      'changer': '/ Đổi giọng (Voice Changer)',
      'lib': '/ Kho giọng đọc (Voice Library)'
    };

    function switchTool(toolId) {
      // 1. Update Sidebar Active
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      const activeNav = document.getElementById('nav-' + toolId);
      if (activeNav) activeNav.classList.add('active');

      // 2. Update Breadcrumb
      document.getElementById('crumb-tool').innerText = TOOL_TITLES[toolId] || '';

      // 3. Show/Hide Workspace screens
      ['tts', 'vc', 'changer', 'lib'].forEach(id => {
        const el = document.getElementById('ws-' + id);
        if (el) el.style.display = (id === toolId) ? 'flex' : 'none';
      });

      // 4. Show/Hide Settings Panel (Visible for tts and changer)
      const inspector = document.getElementById('inspector');
      if (toolId === 'tts' || toolId === 'changer') {
        inspector.style.display = 'flex';
      } else {
        inspector.style.display = 'none';
      }
    }

    function switchVcTab(tabId) {
      document.getElementById('vc-tab-clone').classList.toggle('active', tabId === 'clone');
      document.getElementById('vc-tab-design').classList.toggle('active', tabId === 'design');
      document.getElementById('vc-pane-clone').style.display = (tabId === 'clone') ? 'flex' : 'none';
      document.getElementById('vc-pane-design').style.display = (tabId === 'design') ? 'flex' : 'none';
    }

    function filterVoices(cat, btn) {
      document.querySelectorAll('.vlib-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');

      document.querySelectorAll('.vlib-card').forEach(card => {
        const tags = card.getAttribute('data-tags') || '';
        if (cat === 'all' || tags.includes(cat)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function useVoice(id, name, toneClass, desc) {
      // Update Inspector
      const orb = document.getElementById('inspector-orb');
      orb.className = 'voice-orb ' + toneClass;
      document.getElementById('inspector-name').innerText = name;
      document.getElementById('inspector-desc').innerText = desc;

      // Update Changer Target
      const chOrb = document.getElementById('changer-target-orb');
      if (chOrb) chOrb.className = 'voice-orb ' + toneClass;
      const chName = document.getElementById('changer-target-name');
      if (chName) chName.innerText = name;

      // Switch to TTS
      switchTool('tts');
    }

    function insertTag(tag) {
      const ta = document.getElementById('script-input');
      const start = ta.selectionStart;
      const end = ta.selectionEnd;
      const val = ta.value;
      const before = val.substring(0, start);
      const after = val.substring(end, val.length);
      const prefix = (start > 0 && val[start - 1] !== '\\n' && val[start - 1] !== ' ') ? ' ' : '';
      const suffix = (after.length > 0 && after[0] !== ' ' && after[0] !== '\\n') ? ' ' : ' ';
      ta.value = before + prefix + tag + suffix + after;
      const newPos = start + prefix.length + tag.length + suffix.length;
      ta.setSelectionRange(newPos, newPos);
      ta.focus();
      updateCount();
    }

    function updateCount() {
      const ta = document.getElementById('script-input');
      document.getElementById('char-count').innerText = ta.value.length.toLocaleString('vi-VN') + ' / 5.000 ký tự';
    }

    function clearScript() {
      document.getElementById('script-input').value = '';
      updateCount();
    }

    function restoreSampleScript() {
      const sample = `[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.\\n[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.\\n[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số trên GPU GTX 1650.\\n[điềm tĩnh] Cảm ơn bạn đã lắng nghe.`;
      document.getElementById('script-input').value = sample;
      updateCount();
    }

    let countdownTimer = null;
    let secondsLeft = 10;

    function triggerGenerate() {
      const dock = document.getElementById('output-dock');
      dock.style.display = 'flex';
      secondsLeft = 10;
      document.getElementById('countdown-chip').innerText = '10s';
      
      clearInterval(countdownTimer);
      countdownTimer = setInterval(() => {
        secondsLeft--;
        if (secondsLeft <= 0) {
          clearInterval(countdownTimer);
          dismissDock();
        } else {
          document.getElementById('countdown-chip').innerText = secondsLeft + 's';
        }
      }, 1000);
    }

    function dismissDock() {
      clearInterval(countdownTimer);
      document.getElementById('output-dock').style.display = 'none';
    }

    function togglePopover(id) {
      const menu = document.getElementById(id);
      const isOpen = menu.classList.contains('open');
      document.querySelectorAll('.el-fx-popover').forEach(m => m.classList.remove('open'));
      if (!isOpen) menu.classList.add('open');
    }

    function setFx(targetId, val, optEl) {
      document.getElementById(targetId).innerText = val;
      const popover = optEl.parentElement;
      popover.querySelectorAll('.el-fx-opt').forEach(el => el.classList.remove('active'));
      optEl.classList.add('active');
      popover.classList.remove('open');
    }

    window.onclick = function(e) {
      if (!e.target.closest('.el-fx-select-cell') && !e.target.closest('.el-fx-popover')) {
        document.querySelectorAll('.el-fx-popover').forEach(m => m.classList.remove('open'));
      }
    };
  </script>
</body>
</html>
"""
    with open('E:/VoiceAI/studio_mockup.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated studio_mockup.html with size: {len(html)} characters")

if __name__ == '__main__':
    generate_full_mockup()
