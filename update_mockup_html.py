import re

with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update fx-opt check styling in CSS
old_fx_check_css = """.el-fx-opt .fx-check {
      opacity: 0;
      color: var(--accent);
    }
    .el-fx-opt.active .fx-check { opacity: 1; }"""

new_fx_check_css = """.el-fx-opt {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 7px 12px;
      font-size: 12.5px;
      color: #18181b;
      cursor: pointer;
      border-radius: 6px;
      transition: background 0.12s ease;
    }
    .el-fx-opt:hover {
      background: #f4f4f5;
    }
    .el-fx-opt .fx-check {
      display: none;
      color: #18181b;
    }
    .el-fx-opt.active .fx-check {
      display: block;
    }"""

if old_fx_check_css in html:
    html = html.replace(old_fx_check_css, new_fx_check_css)
    print("Replaced fx check CSS successfully")
else:
    print("Could not find exact old_fx_check_css, appending rule")
    html = html.replace("/* 2.3. RIGHT INSPECTOR (SETTINGS) */", new_fx_check_css + "\n/* 2.3. RIGHT INSPECTOR (SETTINGS) */")

# 2. Update HTML block from <!-- 4 Sliders matching Image 2 --> to <!-- Reset Button -->
target_start = "<!-- 4 Sliders matching Image 2 -->"
target_end = "<!-- Reset Button -->"

new_sliders_html = """<!-- 4 Sliders matching Image 1 & 2 -->
        <!-- 1. Tốc độ đọc -->
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

        <!-- 2. Độ ổn định -->
        <div class="slider-card">
          <div class="slider-header">
            <span class="slider-title">Độ ổn định</span>
          </div>
          <div class="slider-sub-labels">
            <span>Linh hoạt, cảm xúc</span>
            <div class="slider-right-col">
              <span class="slider-tick-indicator">v</span>
              <span>Ổn định, đều đặn</span>
            </div>
          </div>
          <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.45" style="--val: 45%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
        </div>

        <!-- 3. Độ bám giọng mẫu -->
        <div class="slider-card">
          <div class="slider-header">
            <span class="slider-title">Độ bám giọng mẫu</span>
          </div>
          <div class="slider-sub-labels">
            <span>Linh hoạt</span>
            <div class="slider-right-col">
              <span class="slider-tick-indicator">v</span>
              <span>Rất giống mẫu</span>
            </div>
          </div>
          <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.75" style="--val: 75%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
        </div>

        <!-- 4. Nhấn nhá cảm xúc -->
        <div class="slider-card">
          <div class="slider-header">
            <span class="slider-title">Nhấn nhá cảm xúc</span>
          </div>
          <div class="slider-sub-labels">
            <span>Tự nhiên</span>
            <div class="slider-right-col">
              <span class="slider-tick-indicator">v</span>
              <span>Kịch tính</span>
            </div>
          </div>
          <input type="range" class="el-range-input" min="0.0" max="1.0" step="0.05" value="0.05" style="--val: 5%;" oninput="this.style.setProperty('--val', (this.value * 100) + '%');">
        </div>

        <!-- Audio effects matching Image 2 -->
        <div class="el-fx-section">
          <div class="el-fx-header" onclick="document.getElementById('fx-body').classList.toggle('collapsed')">
            <span class="el-fx-title">Audio effects</span>
            <svg class="el-fx-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="el-fx-body" id="fx-body">
            
            <!-- Row 1: Distance -->
            <div class="el-fx-row" id="fx-row-dist">
              <div class="el-fx-label-cell">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="11" r="2.5"/><path d="M12 13.5v4.5"/><path d="M9.5 18h5"/><path d="M6.5 7.5a7.5 7.5 0 0 0 0 7" stroke-dasharray="2 2"/><path d="M17.5 7.5a7.5 7.5 0 0 1 0 7" stroke-dasharray="2 2"/></svg>
                <span>Distance</span>
              </div>
              <div class="el-fx-select-cell" onclick="togglePopover('menu-dist', event)">
                <span id="txt-dist">Far</span>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"/></svg>
              </div>
              <div class="el-fx-remove-cell" onclick="document.getElementById('fx-row-dist').style.display='none'" title="Gỡ hiệu ứng">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              </div>

              <!-- Distance Popover -->
              <div class="el-fx-popover" id="menu-dist">
                <div class="el-fx-opt" onclick="selectFx('txt-dist', 'Near', this)">
                  <span>Near</span>
                  <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="el-fx-opt" onclick="selectFx('txt-dist', 'Medium', this)">
                  <span>Medium</span>
                  <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="el-fx-opt active" onclick="selectFx('txt-dist', 'Far', this)">
                  <span>Far</span>
                  <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
              </div>
            </div>

            <!-- Row 2: Space -->
            <div class="el-fx-row" id="fx-row-space">
              <div class="el-fx-label-cell">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v3"/></svg>
                <span>Space</span>
              </div>
              <div class="el-fx-select-cell" onclick="togglePopover('menu-space', event)">
                <span id="txt-space">Studio (Dry)</span>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
              <div class="el-fx-remove-cell" onclick="document.getElementById('fx-row-space').style.display='none'" title="Gỡ hiệu ứng">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              </div>

              <!-- Space Popover -->
              <div class="el-fx-popover" id="menu-space">
                <div class="el-fx-opt active" onclick="selectFx('txt-space', 'Studio (Dry)', this)"><span>Studio (Dry)</span><svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                <div class="el-fx-opt" onclick="selectFx('txt-space', 'Small Room', this)"><span>Small Room</span><svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                <div class="el-fx-opt" onclick="selectFx('txt-space', 'Large Hall', this)"><span>Large Hall</span><svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
                <div class="el-fx-opt" onclick="selectFx('txt-space', 'Phone Line', this)"><span>Phone Line</span><svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>
              </div>
            </div>

          </div>
        </div>

        <!-- Language row matching Image 1 -->
        <div class="control-row">
          <span class="control-row-label">Ngôn ngữ</span>
          <div class="el-lang-outer-box" onclick="alert('Ngôn ngữ: English / Tiếng Việt / Tự động')">
            <span class="el-lang-badge">English <span class="el-lang-caret">▼</span></span>
          </div>
        </div>

        <!-- Master switch matching Image 1 with outer box -->
        <div class="control-row">
          <span class="control-row-label">Master chuẩn phòng thu (-14 LUFS)</span>
          <div class="toggle-outer-box">
            <label class="toggle-switch">
              <input type="checkbox" checked>
              <span class="slider-toggle"></span>
            </label>
          </div>
        </div>

        <!-- Denoise switch matching Image 1 with outer box -->
        <div class="control-row">
          <span class="control-row-label">Loại bỏ tiếng ồn nền</span>
          <div class="toggle-outer-box">
            <label class="toggle-switch">
              <input type="checkbox">
              <span class="slider-toggle"></span>
            </label>
          </div>
        </div>

        <!-- Output format pill matching Image 1 -->
        <div class="control-row">
          <span class="control-row-label">Định dạng đầu ra</span>
          <span class="output-format-badge">WAV · 24 kHz · TruePeak -1.0dB</span>
        </div>

        """

start_pos = html.find(target_start)
end_pos = html.find(target_end)

if start_pos != -1 and end_pos != -1:
    html = html[:start_pos] + new_sliders_html + html[end_pos:]
    print("Replaced Inspector controls HTML successfully")
else:
    print(f"Could not find boundaries: start={start_pos}, end={end_pos}")

# 3. Add Sample restoration button in footer of script
old_btn_clear = """            <button class="btn-clear" onclick="clearScript()" title="Xóa toàn bộ văn bản">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
              Xóa
            </button>"""

new_btn_actions = """            <button class="btn-clear" onclick="clearScript()" title="Xóa toàn bộ văn bản">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
              Xóa
            </button>
            <button class="btn-clear" onclick="restoreSampleScript()" title="Khôi phục kịch bản mẫu">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              Mẫu
            </button>"""

if old_btn_clear in html:
    html = html.replace(old_btn_clear, new_btn_actions)
    print("Added Sample restoration button successfully")

# 4. Add restoreSampleScript function
old_script_func = "function clearScript() {"
new_script_func = """function restoreSampleScript() {
      const sample = `[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.\\n[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.\\n[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số.\\n[điềm tĩnh] Cảm ơn bạn đã lắng nghe.`;
      document.getElementById('script-input').value = sample;
      updateCount();
    }

    function clearScript() {"""

if old_script_func in html and "restoreSampleScript" not in html:
    html = html.replace(old_script_func, new_script_func)
    print("Added restoreSampleScript JS function")

with open('E:/VoiceAI/studio_mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished writing studio_mockup.html")
