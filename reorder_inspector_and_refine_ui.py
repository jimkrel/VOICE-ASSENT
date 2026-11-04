import re

APP_PATH = r"E:\VoiceAI\studio_app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update PRESETS keys for clean display matching Image 1
text = text.replace(
    '"Hope — ElevenLabs (American Female • ✨ Upbeat & Clear)":',
    '"Hope — upbeat and clear":'
)
text = text.replace(
    '"Marcus — Documentary & Crime (US Deep Male)":',
    '"Marcus — documentary and crime":'
)
text = text.replace(
    '"Liam — Storyteller & Essay (US Conversational)":',
    '"Liam — storyteller and essay":'
)
text = text.replace(
    '"Alex — Movie Recap & Shorts (US Punchy & Fast)":',
    '"Alex — movie recap and shorts":'
)
text = text.replace(
    '"Emma — Explainer & Podcast (UK Warm Female)":',
    '"Emma — explainer and podcast":'
)

# 2. Extract Inspector block and reorganize elements
# Find the Tab("Cài đặt") content
tab_start = 'with gr.Tab("Cài đặt"):'
tab_end = 'with gr.Tab("Lịch sử"):'

tab_content = text[text.find(tab_start):text.find(tab_end)]

new_tab_content = '''with gr.Tab("Cài đặt"):
                            gr.HTML('<div class="el-sec-title">Giọng đọc</div>')
                            with gr.Row(elem_classes="el-voice-pill-row"):
                                voice_dd = gr.Dropdown(
                                    choices=voice_choices(),
                                    value=voice_choices()[0],
                                    show_label=False,
                                    container=False,
                                    elem_classes="el-pill-dd",
                                    elem_id="voice_dd_input",
                                )
                            voice_sample_quote = gr.HTML(render_voice_preview_quote(voice_choices()[0]))
                            voice_sample_player = gr.Audio(
                                value=all_voices()[voice_choices()[0]]["audio"],
                                label="▶ Nghe thử mẫu giọng đang chọn",
                                interactive=False,
                                autoplay=False,
                                elem_id="voice_sample_audio_player",
                                visible=False,
                            )

                            # Tốc độ
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Tốc độ đọc</span><span class="el-slider-val" id="val-speed">0.95x</span></div>
                              <div class="sub-row"><span>Chậm hơn</span><span>Nhanh hơn</span></div>
                            </div>""")
                            speed = gr.Slider(0.7, 1.4, value=0.95, step=0.05, show_label=False, container=False, elem_id="slider_speed", elem_classes="el-clean-slider")

                            # Độ ổn định
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Độ ổn định</span><span class="el-slider-val" id="val-stability">45%</span></div>
                              <div class="sub-row"><span>Linh hoạt, cảm xúc</span><span>Ổn định, đều đặn</span></div>
                            </div>""")
                            stability = gr.Slider(0.0, 1.0, value=0.45, step=0.05, show_label=False, container=False, elem_id="slider_stability", elem_classes="el-clean-slider")

                            # Độ tương đồng
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Độ bám giọng mẫu</span><span class="el-slider-val" id="val-similarity">75%</span></div>
                              <div class="sub-row"><span>Linh hoạt</span><span>Rất giống mẫu</span></div>
                            </div>""")
                            similarity = gr.Slider(0.0, 1.0, value=0.75, step=0.05, show_label=False, container=False, elem_id="slider_similarity", elem_classes="el-clean-slider")

                            # Cường điệu phong cách
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Nhấn nhá cảm xúc</span><span class="el-slider-val" id="val-style">5%</span></div>
                              <div class="sub-row"><span>Tự nhiên</span><span>Kịch tính</span></div>
                            </div>""")
                            style_exag = gr.Slider(0.0, 1.0, value=0.05, step=0.05, show_label=False, container=False, elem_id="slider_style", elem_classes="el-clean-slider")

                            # ==================== ElevenLabs Audio effects ====================
                            gr.HTML("""
                            <div class="el-fx-section">
                              <div class="el-fx-header" onclick="toggleFxSection(this)">
                                <span class="el-fx-title">Audio effects</span>
                                <svg class="el-fx-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                              </div>
                              <div class="el-fx-body">
                                <!-- Row 1: Distance (Near / Medium / Far) -->
                                <div class="el-fx-row" id="fx-row-distance">
                                  <div class="el-fx-label-cell">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                      <circle cx="12" cy="11" r="2.5"/>
                                      <path d="M12 13.5v4.5"/>
                                      <path d="M9.5 18h5"/>
                                      <path d="M6.5 7.5a7.5 7.5 0 0 0 0 7" stroke-dasharray="2 2"/>
                                      <path d="M17.5 7.5a7.5 7.5 0 0 1 0 7" stroke-dasharray="2 2"/>
                                    </svg>
                                    <span>Distance</span>
                                  </div>
                                  <div class="el-fx-select-cell" id="fx-cell-distance" onclick="toggleFxDropdown('distance', event)">
                                    <span id="fx-val-distance">Medium</span>
                                    <svg class="fx-dd-arrow" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                                  </div>
                                  <div class="el-fx-remove-cell" onclick="removeFxRow('distance', event)" title="Gỡ hiệu ứng Distance">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                                  </div>
                                  <!-- Popover menu -->
                                  <div class="el-fx-popover" id="fx-menu-distance">
                                    <div class="el-fx-opt" data-val="Near" onclick="selectFxOption('distance', 'Near', this, event)">
                                      <span>Near</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt active" data-val="Medium" onclick="selectFxOption('distance', 'Medium', this, event)">
                                      <span>Medium</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Far" onclick="selectFxOption('distance', 'Far', this, event)">
                                      <span>Far</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                  </div>
                                </div>

                                <!-- Row 2: Space & Filter -->
                                <div class="el-fx-row" id="fx-row-env">
                                  <div class="el-fx-label-cell">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                      <path d="M2 10v3"/>
                                      <path d="M6 6v11"/>
                                      <path d="M10 3v18"/>
                                      <path d="M14 8v7"/>
                                      <path d="M18 5v13"/>
                                      <path d="M22 10v3"/>
                                    </svg>
                                    <span>Space</span>
                                  </div>
                                  <div class="el-fx-select-cell" id="fx-cell-env" onclick="toggleFxDropdown('env', event)">
                                    <span id="fx-val-env">Studio (Dry)</span>
                                    <svg class="fx-dd-arrow" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                                  </div>
                                  <div class="el-fx-remove-cell" onclick="removeFxRow('env', event)" title="Gỡ hiệu ứng Space">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                                  </div>
                                  <!-- Popover menu -->
                                  <div class="el-fx-popover" id="fx-menu-env">
                                    <div class="el-fx-opt active" data-val="Studio (Dry)" onclick="selectFxOption('env', 'Studio (Dry)', this, event)">
                                      <span>Studio (Dry)</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Small Room" onclick="selectFxOption('env', 'Small Room', this, event)">
                                      <span>Small Room</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Large Hall" onclick="selectFxOption('env', 'Large Hall', this, event)">
                                      <span>Large Hall</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Phone Line" onclick="selectFxOption('env', 'Phone Line', this, event)">
                                      <span>Phone Line</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Vintage Radio" onclick="selectFxOption('env', 'Vintage Radio', this, event)">
                                      <span>Vintage Radio</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Megaphone" onclick="selectFxOption('env', 'Megaphone', this, event)">
                                      <span>Megaphone</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                  </div>
                                </div>

                                <div class="el-fx-add-btn" id="fx-add-btn" onclick="restoreFxRows()">
                                  <span>+ Add effect</span>
                                </div>
                              </div>
                            </div>""")
                            fx_distance = gr.Textbox(value="Medium", show_label=False, container=False, elem_id="fx_distance_input")
                            fx_env = gr.Textbox(value="Studio (Dry)", show_label=False, container=False, elem_id="fx_env_input")

                            # Ngôn ngữ
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Ngôn ngữ</div>')
                                lang = gr.Dropdown(
                                    list(LANG_MAP.keys()),
                                    value="English",
                                    show_label=False,
                                    container=False,
                                    scale=0,
                                    min_width=130,
                                    elem_classes="el-pill-dd",
                                )

                            # Master âm thanh phòng thu (-14 LUFS)
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Master chuẩn phòng thu (-14 LUFS)</div>')
                                speaker_boost = gr.Checkbox(value=True, show_label=False, container=False, scale=0, min_width=44, elem_classes="el-switch")

                            # Loại bỏ tiếng ồn nền
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Loại bỏ tiếng ồn nền</div>')
                                denoise = gr.Checkbox(value=False, show_label=False, container=False, scale=0, min_width=44, elem_classes="el-switch")

                            # Định dạng đầu ra
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Định dạng đầu ra</div>')
                                gr.HTML('<div class="el-format-pill">WAV · 24 kHz · TruePeak -1.0dB</div>')

                            # Nút đặt lại giá trị
                            with gr.Row(elem_classes="el-reset-row"):
                                reset = gr.Button("↺  Đặt lại giá trị", size="sm", elem_classes="btn-reset", scale=0, min_width=110)

                            # Accordion chọn mô hình (Đặt gọn gàng bên dưới các slider chính)
                            with gr.Accordion("⚙️ Cấu hình mô hình tạo sinh (AI Model)", open=False):
                                model_choice_dd = gr.Radio(
                                    choices=[
                                        ("Eleven v4 (Turbo)", "Eleven v4 (Turbo)"),
                                        ("Eleven v3 (Biểu cảm)", "Eleven v3 (Biểu cảm)"),
                                        ("Eleven Multilingual v2 (Chuẩn)", "Eleven Multilingual v2 (Chuẩn)"),
                                    ],
                                    value="Eleven v4 (Turbo)",
                                    show_label=False,
                                    container=False,
                                    elem_id="model_cards_radio",
                                )
                                model_info_card = gr.HTML(render_model_info("Eleven v4 (Turbo)"))
                        '''

text = text.replace(tab_content, new_tab_content)

# 3. Clean up render_voice_preview_quote to be minimal and cohesive
new_quote_func = '''def render_voice_preview_quote(v_name):
    v = all_voices().get(v_name, {})
    text = v.get("text", "")
    desc = v.get("desc", "")
    audio_path = v.get("audio", "").replace(os.sep, "/")
    audio_url = f"/gradio_api/file={audio_path}"
    sname = v_name.split("—")[0].strip()
    return f"""
    <div class="el-sample-quote-card">
      <div class="s-head-row">
        <button class="voice-circle-play-btn" onclick="playVoicePreview('{audio_url}', this)" title="Bấm nghe thử giọng {sname}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
        </button>
        <div class="s-avatar-orb" title="{sname}"></div>
        <div class="s-meta-col">
          <div class="s-desc"><b>{sname}</b> • {desc}</div>
          <div class="s-quote">“{text}”</div>
        </div>
      </div>
    </div>"""'''

text = re.sub(
    r'def render_voice_preview_quote\(v_name\):[\s\S]*?</div>"""',
    new_quote_func,
    text,
    count=1
)

# 4. Refine Textarea styling & card border in CSS
css_refine = """
/* Refined Studio Textarea */
#script {
  border: 1px solid #e2e8f0 !important;
  border-radius: 14px !important;
  background: #ffffff !important;
  padding: 8px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
#script:focus-within {
  border-color: #18181b !important;
  box-shadow: 0 0 0 3px rgba(24, 24, 27, 0.06) !important;
}
#script textarea {
  font-size: 15px !important;
  line-height: 1.65 !important;
  color: #18181b !important;
  background: transparent !important;
  border: none !important;
  padding: 8px 10px !important;
}
"""

if "/* Refined Studio Textarea */" not in text:
    text = text.replace('JS_INJECT = """', css_refine + '\n\nJS_INJECT = """')

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Reordered inspector and refined UI successfully!")
