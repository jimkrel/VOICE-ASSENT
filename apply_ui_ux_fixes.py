import re

APP_PATH = r"E:\VoiceAI\studio_app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. FIX #sidebar justify-content
text = text.replace(
    "justify-content: space-between !important;\n  flex-shrink: 0 !important;\n}",
    "justify-content: flex-start !important;\n  gap: 12px !important;\n  flex-shrink: 0 !important;\n}"
)
text = text.replace(
    "justify-content: space-between !important;\r\n  flex-shrink: 0 !important;\r\n}",
    "justify-content: flex-start !important;\r\n  gap: 12px !important;\r\n  flex-shrink: 0 !important;\r\n}"
)

# 2. FIX .el-logo-brand text color
text = re.sub(
    r'\.el-logo-brand\s*\{[^}]*\}',
    '''.el-logo-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 6px 14px;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #18181b !important;
  border-bottom: 1px solid #e4e4e7;
  margin-bottom: 6px;
}
.el-logo-brand span {
  color: #18181b !important;
  font-weight: 700 !important;
}''',
    text,
    count=1
)

# 3. FIX #model_cards_radio labels and text color (make black/dark, not invisible white!)
text = re.sub(
    r'#model_cards_radio label\s*\{[^}]*\}',
    '''#model_cards_radio label {
  display: flex !important;
  align-items: center !important;
  padding: 8px 12px !important;
  border: 1px solid #e4e4e7 !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #18181b !important;
  margin: 0 !important;
}
#model_cards_radio label span,
#model_cards_radio span,
#model_cards_radio .wrap label {
  color: #18181b !important;
  font-weight: 500 !important;
}''',
    text,
    count=1
)

# 4. FIX #voice_dd_input dropdown background & text
css_dropdown_fix = """
/* Fix voice dropdown styling */
#voice_dd_input,
#voice_dd_input .wrap,
#voice_dd_input .wrap-inner,
#voice_dd_input input,
#voice_dd_input .single-select,
.el-pill-dd,
.el-pill-dd .wrap,
.el-pill-dd .wrap-inner,
.el-pill-dd input,
.el-pill-dd .single-select {
  background: #ffffff !important;
  color: #18181b !important;
  border-color: #e4e4e7 !important;
  border-radius: 12px !important;
}
#voice_dd_input input::placeholder,
.el-pill-dd input::placeholder {
  color: #71717a !important;
}
#voice_dd_input .wrap-inner {
  padding: 6px 10px !important;
}
#voice_sample_audio_player {
  display: none !important;
}
"""

# 5. FIX Top Banner from harsh blue to clean ElevenLabs dark banner
text = text.replace(
    "background: #3d7ff0;",
    "background: #18181b;"
)

# 6. FIX output_dock initial visibility: set visible=False so initially clean!
text = text.replace(
    'with gr.Column(visible=True, elem_classes="el-output-card") as output_dock:',
    'with gr.Column(visible=False, elem_classes="el-output-card") as output_dock:'
)

# 7. ENHANCE .el-emo-toolbar & chips styling
text = re.sub(
    r'\.el-emo-toolbar\s*\{[^}]*\}',
    '''.el-emo-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}
.el-emo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #334155 !important;
}
.el-emo-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  padding: 4px 11px;
  font-size: 12px;
  font-weight: 500;
  color: #0f172a !important;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.el-emo-chip:hover {
  background: #f1f5f9;
  border-color: #0f172a;
  transform: translateY(-1px);
}''',
    text,
    count=1
)

# 8. Append css_dropdown_fix to CSS
if "/* Fix voice dropdown styling */" not in text:
    text = text.replace('JS_INJECT = """', css_dropdown_fix + '\n\nJS_INJECT = """')

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied UI/UX fixes successfully!")
