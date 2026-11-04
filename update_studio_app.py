with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add sample_btn to script actions
old_bottom = """                        with gr.Row(elem_classes="el-bottom"):
                            count = gr.HTML(char_count(""))
                            clear_btn = gr.Button("Xóa", elem_classes="btn-ghost", scale=0, min_width=70)
                            gen_btn = gr.Button("Tạo giọng nói", elem_classes="btn-black", scale=0, min_width=160)"""

new_bottom = """                        with gr.Row(elem_classes="el-bottom"):
                            count = gr.HTML(char_count(""))
                            clear_btn = gr.Button("Xóa", elem_classes="btn-ghost", scale=0, min_width=70)
                            sample_btn = gr.Button("Mẫu", elem_classes="btn-ghost", scale=0, min_width=70)
                            gen_btn = gr.Button("Tạo giọng nói", elem_classes="btn-black", scale=0, min_width=160)"""

if old_bottom in text:
    text = text.replace(old_bottom, new_bottom)
    print("Added sample_btn in bottom row")

# 2. Add sample_btn click binding
old_clear_click = """    clear_btn.click(lambda: "", None, script)"""
new_clear_click = """    clear_btn.click(lambda: "", None, script)
    sample_text_tpl = (
        "[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.\\n"
        "[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.\\n"
        "[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số trên GPU GTX 1650.\\n"
        "[điềm tĩnh] Cảm ơn bạn đã lắng nghe."
    )
    sample_btn.click(lambda: sample_text_tpl, None, script)"""

if old_clear_click in text and "sample_btn.click" not in text:
    text = text.replace(old_clear_click, new_clear_click)
    print("Bound sample_btn click event")

# 3. Update slider headers to have the 'v' tick mark and clean title
old_speed_head = """                            # Tốc độ
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Tốc độ đọc</span><span class=\"el-slider-val\" id=\"val-speed\">0.95x</span></div>
                              <div class=\"sub-row\"><span>Chậm hơn</span><span>Nhanh hơn</span></div>
                            </div>\"\"\")"""

new_speed_head = """                            # Tốc độ
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Tốc độ đọc</span></div>
                              <div class=\"sub-row\"><span>Chậm hơn</span><span class=\"sub-r-wrap\"><span class=\"sub-tick\">v</span><span>Nhanh hơn</span></span></div>
                            </div>\"\"\")"""

if old_speed_head in text:
    text = text.replace(old_speed_head, new_speed_head)
    print("Updated speed head HTML")

old_stab_head = """                            # Độ ổn định
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Độ ổn định</span><span class=\"el-slider-val\" id=\"val-stability\">45%</span></div>
                              <div class=\"sub-row\"><span>Linh hoạt, cảm xúc</span><span>Ổn định, đều đặn</span></div>
                            </div>\"\"\")"""

new_stab_head = """                            # Độ ổn định
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Độ ổn định</span></div>
                              <div class=\"sub-row\"><span>Linh hoạt, cảm xúc</span><span class=\"sub-r-wrap\"><span class=\"sub-tick\">v</span><span>Ổn định, đều đặn</span></span></div>
                            </div>\"\"\")"""

if old_stab_head in text:
    text = text.replace(old_stab_head, new_stab_head)
    print("Updated stability head HTML")

old_sim_head = """                            # Độ tương đồng
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Độ bám giọng mẫu</span><span class=\"el-slider-val\" id=\"val-similarity\">75%</span></div>
                              <div class=\"sub-row\"><span>Linh hoạt</span><span>Rất giống mẫu</span></div>
                            </div>\"\"\")"""

new_sim_head = """                            # Độ tương đồng
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Độ bám giọng mẫu</span></div>
                              <div class=\"sub-row\"><span>Linh hoạt</span><span class=\"sub-r-wrap\"><span class=\"sub-tick\">v</span><span>Rất giống mẫu</span></span></div>
                            </div>\"\"\")"""

if old_sim_head in text:
    text = text.replace(old_sim_head, new_sim_head)
    print("Updated similarity head HTML")

old_style_head = """                            # Cường điệu phong cách
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Nhấn nhá cảm xúc</span><span class=\"el-slider-val\" id=\"val-style\">5%</span></div>
                              <div class=\"sub-row\"><span>Tự nhiên</span><span>Kịch tính</span></div>
                            </div>\"\"\")"""

new_style_head = """                            # Cường điệu phong cách
                            gr.HTML(\"\"\"
                            <div class=\"el-slider-head\">
                              <div class=\"title-row\"><span>Nhấn nhá cảm xúc</span></div>
                              <div class=\"sub-row\"><span>Tự nhiên</span><span class=\"sub-r-wrap\"><span class=\"sub-tick\">v</span><span>Kịch tính</span></span></div>
                            </div>\"\"\")"""

if old_style_head in text:
    text = text.replace(old_style_head, new_style_head)
    print("Updated style head HTML")

# 4. Inject polished CSS for vertical tick thumb & outer toggle border box & sub-tick
new_inspector_polish_css = """
/* ===== POLISHED INSPECTOR MATCHING IMAGE 1 & 2 ===== */
.sub-r-wrap {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  text-align: right !important;
}
.sub-tick {
  font-size: 8px !important;
  color: #a1a1aa !important;
  line-height: 1 !important;
  margin-bottom: 1px !important;
  font-family: ui-monospace, monospace !important;
}
.el-clean-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 3px !important;
  height: 14px !important;
  border-radius: 1px !important;
  background-color: #18181b !important;
  border: none !important;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.4) !important;
  margin-top: -5px !important;
  cursor: pointer !important;
}
.el-clean-slider input[type="range"]::-webkit-slider-runnable-track {
  height: 3px !important;
  border-radius: 2px !important;
  background: linear-gradient(to right, #52525b var(--range_progress, 50%), #e4e4e7 var(--range_progress, 50%)) !important;
  border: none !important;
}
.el-switch {
  border: 1px solid #e5e7eb !important;
  border-radius: 6px !important;
  padding: 3px 5px !important;
  background: #ffffff !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.el-switch input[type="checkbox"] {
  appearance: none !important;
  -webkit-appearance: none !important;
  width: 36px !important;
  height: 19px !important;
  background: #f4f4f5 !important;
  border: 1px solid #e4e4e7 !important;
  border-radius: 20px !important;
  position: relative !important;
  cursor: pointer !important;
  transition: background 0.2s ease, border-color 0.2s ease !important;
}
.el-switch input[type="checkbox"]::after {
  content: "" !important;
  position: absolute !important;
  top: 2px !important;
  left: 2px !important;
  width: 13px !important;
  height: 13px !important;
  border-radius: 50% !important;
  background: #d4d4d8 !important;
  transition: transform 0.2s ease, background-color 0.2s ease !important;
}
.el-switch input[type="checkbox"]:checked {
  background: #000000 !important;
  border-color: #000000 !important;
}
.el-switch input[type="checkbox"]:checked::after {
  background: #ffffff !important;
  transform: translateX(17px) !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.35) !important;
}
.el-format-pill {
  background: #f4f4f5 !important;
  border-radius: 9999px !important;
  padding: 5px 10px !important;
  font-size: 10px !important;
  font-weight: 500 !important;
  color: #27272a !important;
  white-space: nowrap !important;
  border: none !important;
  letter-spacing: -0.01em !important;
}
"""

if "/* ===== POLISHED INSPECTOR MATCHING IMAGE 1 & 2 ===== */" not in text:
    target_css_end = '"""\n\nJS_INJECT = """'
    if target_css_end in text:
        text = text.replace(target_css_end, new_inspector_polish_css + '\n' + target_css_end)
        print("Injected polished CSS into studio_app.py")
    else:
        print("Could not find target_css_end in studio_app.py")

with open('E:/VoiceAI/studio_app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished updating studio_app.py")
