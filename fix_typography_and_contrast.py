with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix title-row missing dot
text = text.replace(
    "\ntitle-row {\n  display: flex;",
    "\n.title-row {\n  display: flex;"
)
text = text.replace(
    "\r\ntitle-row {\r\n  display: flex;",
    "\r\n.title-row {\r\n  display: flex;"
)

# Enhance typography rules
css_typo_enhancement = """
/* High-Contrast Crisp Typography for Inspector Sliders & Labels */
.el-slider-head {
  margin-top: 16px !important;
  margin-bottom: 4px !important;
}
.title-row,
.el-slider-head .title-row {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  margin-bottom: 3px !important;
}
.title-row span,
.el-slider-head .title-row span {
  color: #18181b !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}
.sub-row,
.el-slider-head .sub-row {
  display: flex !important;
  justify-content: space-between !important;
  font-size: 11px !important;
  color: #52525b !important;
}
.sub-row span,
.el-slider-head .sub-row span {
  color: #52525b !important;
  font-size: 11px !important;
  font-weight: 500 !important;
}
.el-slider-val {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  background: #f4f4f5 !important;
  padding: 2px 7px !important;
  border-radius: 6px !important;
  border: 1px solid #e4e4e7 !important;
}
.el-sec-title {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  margin: 14px 0 6px !important;
}
.el-row-label {
  font-size: 12.5px !important;
  font-weight: 500 !important;
  color: #18181b !important;
}
.el-sample-quote-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 10px 12px !important;
  margin: 8px 0 12px !important;
}
.el-sample-quote-card .s-desc,
.el-sample-quote-card .s-desc b {
  color: #0f172a !important;
  font-size: 12px !important;
  font-weight: 600 !important;
}
.el-sample-quote-card .s-quote {
  color: #475569 !important;
  font-size: 11.5px !important;
  font-style: italic !important;
  line-height: 1.4 !important;
  margin-top: 2px !important;
}
"""

# Inject before JS_INJECT
if "/* High-Contrast Crisp Typography for Inspector Sliders & Labels */" not in text:
    text = text.replace('JS_INJECT = """', css_typo_enhancement + '\n\nJS_INJECT = """')

with open(r"E:\VoiceAI\studio_app.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed typography and contrast successfully!")
