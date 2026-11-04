import re

with open('E:/VoiceAI/extracted_ui_design/components/workspace-settings-panel.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update SettingSlider sub-labels
old_slider_sub = """      <span className="mt-1.5 flex items-center justify-between gap-3 text-[10px] text-[#8b8790]">
        <span>{lowLabel}</span>
        <span className="text-right">{highLabel}</span>
      </span>"""

new_slider_sub = """      <span className="mt-1.5 flex items-center justify-between gap-3 text-[10px] text-[#8b8790]">
        <span>{lowLabel}</span>
        <span className="flex flex-col items-end text-right">
          <span className="text-[8px] font-mono text-[#a1a1aa] leading-none mb-0.5">v</span>
          <span>{highLabel}</span>
        </span>
      </span>"""

if old_slider_sub in text:
    text = text.replace(old_slider_sub, new_slider_sub)
    print("Updated SettingSlider sub-labels")

# 2. Update SettingSwitch to have the rectangular outer border and solid black ON state
old_switch = """function SettingSwitch({
  label,
  defaultChecked = false,
}: {
  label: string
  defaultChecked?: boolean
}) {
  const [checked, setChecked] = useState(defaultChecked)

  return (
    <div className="flex items-center justify-between gap-3 py-1.5">
      <span className="text-[11px] font-medium leading-4 text-[#514e56]">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        aria-label={label}
        onClick={() => setChecked((current) => !current)}
        className={cn(
          "relative flex h-5 w-9 shrink-0 items-center rounded-full p-0.5 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
          checked ? "bg-primary" : "bg-muted"
        )}
      >
        <span
          className={cn(
            "absolute left-0.5 size-4 rounded-full bg-white shadow-sm transition-transform duration-200 ease-out",
            checked && "translate-x-4"
          )}
        />
      </button>
    </div>
  )
}"""

new_switch = """function SettingSwitch({
  label,
  defaultChecked = false,
}: {
  label: string
  defaultChecked?: boolean
}) {
  const [checked, setChecked] = useState(defaultChecked)

  return (
    <div className="flex items-center justify-between gap-3 py-1.5">
      <span className="text-[11px] font-medium leading-4 text-[#514e56]">{label}</span>
      <div className="inline-flex items-center justify-center rounded-md border border-[#e5e7eb] p-1 bg-white">
        <button
          type="button"
          role="switch"
          aria-checked={checked}
          aria-label={label}
          onClick={() => setChecked((current) => !current)}
          className={cn(
            "relative flex h-4 w-8 shrink-0 items-center rounded-full transition-colors focus-visible:outline-none",
            checked ? "bg-black" : "bg-[#f4f4f5] border border-[#e4e4e7]"
          )}
        >
          <span
            className={cn(
              "absolute left-0.5 size-3 rounded-full transition-transform duration-200 ease-out",
              checked ? "bg-white translate-x-3.5 shadow-sm" : "bg-[#d4d4d8]"
            )}
          />
        </button>
      </div>
    </div>
  )
}"""

if old_switch in text:
    text = text.replace(old_switch, new_switch)
    print("Updated SettingSwitch with outer rectangular border box")

# 3. Update Language selector and Output format badge
old_lang_and_format = """            <div className="border-t border-[#eeece9] pt-3">
              <label className="flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-[#514e56]">Ngôn ngữ</span>
                <select defaultValue="Tự động" className="h-8 max-w-[140px] rounded-lg border border-[#e8e5e1] bg-white px-2 text-[10px] text-[#514e56] outline-none focus:border-[#b8b0e9]">
                  <option>English</option>
                  <option>Tiếng Việt</option>
                  <option>Tự động</option>
                </select>
              </label>
              <div className="mt-2"><SettingSwitch label="Chuẩn âm lượng phòng thu (-14 LUFS)" defaultChecked /></div>
              <div className="mt-1"><SettingSwitch label="Giảm tiếng ồn nền" /></div>
              <label className="mt-3 flex flex-col gap-1.5">
                <span className="text-[11px] font-medium text-[#514e56]">Định dạng đầu ra</span>
                <select defaultValue="WAV · 24 kHz" className="h-9 w-full rounded-lg border border-[#e8e5e1] bg-white px-2.5 text-[10px] text-[#514e56] outline-none focus:border-[#b8b0e9]">
                  <option>WAV · 24 kHz</option>
                  <option>MP3 · 44.1 kHz · 128 kbps</option>
                  <option>WAV · 48 kHz</option>
                </select>
              </label>
            </div>"""

new_lang_and_format = """            <div className="border-t border-[#eeece9] pt-3">
              <div className="flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-[#514e56]">Ngôn ngữ</span>
                <div className="inline-flex items-center gap-1 rounded-lg border border-[#e5e7eb] bg-white p-1 cursor-pointer">
                  <span className="rounded bg-[#2563eb] px-2 py-0.5 text-[10.5px] font-semibold text-white">
                    English ▼
                  </span>
                </div>
              </div>
              <div className="mt-2"><SettingSwitch label="Master chuẩn phòng thu (-14 LUFS)" defaultChecked /></div>
              <div className="mt-1"><SettingSwitch label="Loại bỏ tiếng ồn nền" /></div>
              <div className="mt-2.5 flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-[#514e56]">Định dạng đầu ra</span>
                <span className="rounded-full bg-[#f4f4f5] px-2.5 py-1 text-[10px] font-medium text-[#27272a] whitespace-nowrap">
                  WAV · 24 kHz · TruePeak -1.0dB
                </span>
              </div>
            </div>"""

if old_lang_and_format in text:
    text = text.replace(old_lang_and_format, new_lang_and_format)
    print("Updated language selector and output format badge")

with open('E:/VoiceAI/extracted_ui_design/components/workspace-settings-panel.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished polishing workspace-settings-panel.tsx")
