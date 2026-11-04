with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add "Mẫu" button next to "Xóa"
old_actions = """            <div class="editor-actions">
              <button class="btn-ghost" onclick="clearScript()">Xóa</button>
              <button class="btn-black" onclick="triggerGenerate()">"""

new_actions = """            <div class="editor-actions">
              <button class="btn-ghost" onclick="clearScript()">Xóa</button>
              <button class="btn-ghost" onclick="restoreSampleScript()" title="Khôi phục kịch bản mẫu">Mẫu</button>
              <button class="btn-black" onclick="triggerGenerate()">"""

if old_actions in text:
    text = text.replace(old_actions, new_actions)
    print("Added Mẫu button successfully")

# 2. Fix wrapping of Định dạng đầu ra
old_control_row = """.control-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 36px;
    }"""

new_control_row = """.control-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      min-height: 36px;
    }
    .control-row-label {
      font-size: 11px;
      font-weight: 500;
      color: #3f3f46;
      white-space: nowrap;
      flex-shrink: 0;
    }"""

if old_control_row in text:
    text = text.replace(old_control_row, new_control_row)
    print("Updated control-row CSS successfully")

# 3. Update output-format-badge
old_badge = """.output-format-badge {
      font-size: 10.5px;
      font-weight: 500;
      color: #27272a;
      background: #f4f4f5;
      border: none;
      border-radius: 9999px;
      padding: 6px 14px;
      letter-spacing: -0.01em;
    }"""

new_badge = """.output-format-badge {
      font-size: 10px;
      font-weight: 500;
      color: #27272a;
      background: #f4f4f5;
      border: none;
      border-radius: 9999px;
      padding: 5px 10px;
      letter-spacing: -0.01em;
      white-space: nowrap;
    }"""

if old_badge in text:
    text = text.replace(old_badge, new_badge)
    print("Updated output-format-badge CSS successfully")

with open('E:/VoiceAI/studio_mockup.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished polishing studio_mockup.html")
