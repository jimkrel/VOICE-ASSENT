panel_code = '''"use client"

import { useState } from "react"
import type { CSSProperties } from "react"
import {
  AudioLines,
  Check,
  ChevronDown,
  ChevronUp,
  CircleHelp,
  MinusCircle,
  Radio,
  RotateCcw,
  Volume2,
  Waves,
} from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getVoiceById, voiceCatalog, type VoiceProfile } from "@/lib/voice-catalog"
import { cn } from "@/lib/utils"

type SettingsTool = "text-to-speech" | "voice-changer"

type SettingSliderProps = {
  label: string
  lowLabel: string
  highLabel: string
  min: number
  max: number
  step: number
  defaultValue: number
  formatValue: (value: number) => string
}

function SettingSlider({
  label,
  lowLabel,
  highLabel,
  min,
  max,
  step,
  defaultValue,
  formatValue,
}: SettingSliderProps) {
  const [value, setValue] = useState(defaultValue)
  const progress = ((value - min) / (max - min)) * 100

  return (
    <label className="block">
      <span className="text-[12px] font-semibold text-[#18181b]">
        {label}
      </span>
      <span className="mt-1 flex items-end justify-between gap-3 text-[10.5px] text-[#71717a]">
        <span>{lowLabel}</span>
        <span className="flex flex-col items-end text-right">
          <span className="text-[8px] font-mono text-[#a1a1aa] leading-none mb-0.5">v</span>
          <span>{highLabel}</span>
        </span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) => setValue(Number(event.target.value))}
        aria-label={label}
        aria-valuetext={formatValue(value)}
        style={{ "--range-progress": `${progress}%` } as CSSProperties}
        className="voice-range mt-1.5 w-full"
      />
    </label>
  )
}

function SettingSwitch({
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
}

function EffectRow({
  title,
  icon: Icon,
  options,
  defaultValue,
  onRemove,
}: {
  title: string
  icon: any
  options: string[]
  defaultValue: string
  onRemove: () => void
}) {
  const [currentVal, setCurrentVal] = useState(defaultValue)
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="relative mb-2">
      <div className="flex h-10 items-center rounded-xl border border-[#e5e7eb] bg-white transition hover:border-[#d4cef0]">
        <div className="flex h-full w-[96px] shrink-0 items-center gap-1.5 border-r border-[#eeece9] px-2.5 text-[11px] font-medium text-[#6b7280]">
          <Icon className="size-3.5 text-[#6b7280]" aria-hidden="true" />
          <span>{title}</span>
        </div>
        <button
          type="button"
          onClick={() => setIsOpen((prev) => !prev)}
          className="flex h-full flex-1 items-center justify-between px-3 text-[11.5px] font-medium text-[#111827] outline-none"
        >
          <span>{currentVal}</span>
          {isOpen ? (
            <ChevronUp className="size-3.5 text-[#6b7280]" />
          ) : (
            <ChevronDown className="size-3.5 text-[#6b7280]" />
          )}
        </button>
        <button
          type="button"
          onClick={onRemove}
          aria-label={`Gỡ hiệu ứng ${title}`}
          className="flex size-9 shrink-0 items-center justify-center text-[#9ca3af] hover:text-[#dc2626]"
        >
          <MinusCircle className="size-4" aria-hidden="true" />
        </button>
      </div>

      {isOpen && (
        <div className="absolute left-[70px] right-0 top-11 z-50 rounded-xl border border-[#e5e7eb] bg-white p-1 shadow-xl">
          {options.map((opt) => (
            <button
              key={opt}
              type="button"
              onClick={() => {
                setCurrentVal(opt)
                setIsOpen(false)
              }}
              className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-[11.5px] text-[#111827] transition hover:bg-[#f9fafb]"
            >
              <span>{opt}</span>
              {currentVal === opt && <Check className="size-3.5 text-[#111827]" />}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function VoiceOrb({ tone = "aqua", className }: { tone?: VoiceProfile["tone"]; className?: string }) {
  const orbStyles: Record<string, string> = {
    aqua: "bg-[radial-gradient(circle_at_30%_25%,#e3ffff_0%,#64d8ec_28%,#3b83ee_62%,#8755dc_100%)]",
    violet: "bg-[radial-gradient(circle_at_30%_25%,#f3dcff_0%,#b772e2_30%,#5147cc_68%,#312a63_100%)]",
    coral: "bg-[radial-gradient(circle_at_30%_25%,#fff1df_0%,#ff9c70_30%,#df5d74_64%,#684cb9_100%)]",
    blue: "bg-[radial-gradient(circle_at_30%_25%,#d8f7ff_0%,#52c0e9_32%,#2575c8_68%,#183b78_100%)]",
    green: "bg-[radial-gradient(circle_at_30%_25%,#e7fff2_0%,#76d9b0_30%,#398db5_66%,#566fda_100%)]",
  }

  return (
    <span
      aria-hidden="true"
      className={cn(
        "block size-9 shrink-0 rounded-full border border-white/70 shadow-[0_2px_8px_rgba(35,69,120,0.18)]",
        orbStyles[tone] || orbStyles.aqua,
        className
      )}
    />
  )
}

function SettingsContent({
  activeTool,
  selectedVoiceId,
  onSelectVoice,
}: {
  activeTool: SettingsTool
  selectedVoiceId: string
  onSelectVoice: (id: string) => void
}) {
  const selectedVoice = getVoiceById(selectedVoiceId)
  const [visibleEffects, setVisibleEffects] = useState(["Distance", "Space"])
  const [resetKey, setResetKey] = useState(0)

  function resetSettings() {
    setResetKey((current) => current + 1)
    setVisibleEffects(["Distance", "Space"])
  }

  return (
    <div className="flex flex-col gap-4 pb-5 pt-3">
      {/* Voice Selection */}
      <section aria-label="Chọn giọng đọc" className="flex flex-col gap-2">
        <label htmlFor="settings-voice" className="text-[12px] font-semibold text-[#18181b]">
          Giọng đọc
        </label>
        <div className="relative block">
          <select
            id="settings-voice"
            value={selectedVoice.id}
            onChange={(event) => onSelectVoice(event.target.value)}
            className="h-10 w-full appearance-none rounded-xl border border-[#e7e4e0] bg-white pl-3 pr-9 text-[11.5px] font-medium text-[#18181b] outline-none transition focus:border-[#b8b0e9] focus:ring-2 focus:ring-[#efedff]"
          >
            {voiceCatalog.map((voice) => (
              <option key={voice.id} value={voice.id}>{`${voice.name} — ${voice.style}`}</option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-[#8b8790]" aria-hidden="true" />
        </div>
        <div className="flex items-center gap-3 rounded-xl bg-[#f8f7f5] p-3 border border-[#eeece9]">
          <VoiceOrb tone={selectedVoice.tone} />
          <div className="min-w-0">
            <p className="truncate text-[11.5px] font-semibold text-[#18181b]">
              {selectedVoice.name} · {selectedVoice.locale} · {selectedVoice.gender}
            </p>
            <p className="mt-0.5 truncate text-[10.5px] text-[#71717a]">{selectedVoice.description}</p>
            <p className="mt-0.5 text-[10px] text-[#8b8790]">
              {activeTool === "voice-changer" ? "Giọng đích cho tệp âm thanh" : "Giọng dùng cho kịch bản"}
            </p>
          </div>
        </div>
      </section>

      <div key={resetKey} className="flex flex-col gap-3.5">
        {/* Tốc độ đọc (Always visible) */}
        <SettingSlider
          label="Tốc độ đọc"
          lowLabel="Chậm hơn"
          highLabel="Nhanh hơn"
          min={0.7}
          max={1.4}
          step={0.05}
          defaultValue={0.95}
          formatValue={(value) => `${value.toFixed(2)}x`}
        />

        {/* Accordion Tùy chỉnh nâng cao */}
        <details className="motion-disclosure group rounded-xl border border-[#e8e5e1] bg-white p-3.5" open>
          <summary className="flex cursor-pointer list-none items-center justify-between gap-3 text-[12px] font-semibold text-[#18181b]">
            Tùy chỉnh nâng cao
            <ChevronDown className="size-4 text-[#8b8790] transition-transform group-open:rotate-180" aria-hidden="true" />
          </summary>
          <div className="mt-4 flex flex-col gap-3.5">
            <SettingSlider
              label="Độ ổn định"
              lowLabel="Linh hoạt, cảm xúc"
              highLabel="Ổn định, đều đặn"
              min={0}
              max={100}
              step={5}
              defaultValue={45}
              formatValue={(value) => `${value}%`}
            />
            <SettingSlider
              label="Độ bám giọng mẫu"
              lowLabel="Linh hoạt"
              highLabel="Rất giống mẫu"
              min={0}
              max={100}
              step={5}
              defaultValue={75}
              formatValue={(value) => `${value}%`}
            />
            <SettingSlider
              label="Nhấn nhá cảm xúc"
              lowLabel="Tự nhiên"
              highLabel="Kịch tính"
              min={0}
              max={100}
              step={5}
              defaultValue={5}
              formatValue={(value) => `${value}%`}
            />

            {/* Audio effects (Image 2) */}
            <div className="border-t border-[#eeece9] pt-3">
              <div className="mb-2.5 flex items-center justify-between text-[11.5px] font-semibold text-[#18181b]">
                <span>Audio effects</span>
                <ChevronDown className="size-3.5 text-[#8b8790]" />
              </div>
              <div className="flex flex-col gap-1.5">
                {visibleEffects.includes("Distance") ? (
                  <EffectRow
                    title="Distance"
                    icon={Radio}
                    options={["Near", "Medium", "Far"]}
                    defaultValue="Far"
                    onRemove={() => setVisibleEffects((current) => current.filter((effect) => effect !== "Distance"))}
                  />
                ) : null}
                {visibleEffects.includes("Space") ? (
                  <EffectRow
                    title="Space"
                    icon={Waves}
                    options={["Studio (Dry)", "Small Room", "Large Hall", "Phone Line"]}
                    defaultValue="Studio (Dry)"
                    onRemove={() => setVisibleEffects((current) => current.filter((effect) => effect !== "Space"))}
                  />
                ) : null}
              </div>
              {visibleEffects.length === 0 ? (
                <button
                  type="button"
                  onClick={() => setVisibleEffects(["Distance", "Space"])}
                  className="mt-1 text-[10.5px] font-medium text-[#6256c6] underline underline-offset-2"
                >
                  + Thêm lại hiệu ứng
                </button>
              ) : null}
            </div>

            {/* Language & Toggles (Image 1) */}
            <div className="border-t border-[#eeece9] pt-3">
              <div className="flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-[#514e56]">Ngôn ngữ</span>
                <div className="inline-flex items-center gap-1 rounded-lg border border-[#e5e7eb] bg-white p-1 cursor-pointer">
                  <span className="rounded bg-[#2563eb] px-2 py-0.5 text-[10.5px] font-semibold text-white">
                    English ▼
                  </span>
                </div>
              </div>
              <div className="mt-2.5"><SettingSwitch label="Master chuẩn phòng thu (-14 LUFS)" defaultChecked /></div>
              <div className="mt-1"><SettingSwitch label="Loại bỏ tiếng ồn nền" /></div>
              <div className="mt-2.5 flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-[#514e56]">Định dạng đầu ra</span>
                <span className="rounded-full bg-[#f4f4f5] px-2.5 py-1 text-[10px] font-medium text-[#27272a] whitespace-nowrap">
                  WAV · 24 kHz · TruePeak -1.0dB
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={resetSettings}
              className="mt-1 flex h-8 items-center justify-center gap-1.5 rounded-lg border border-[#e8e5e1] text-[11px] font-medium text-[#625e67] transition-colors hover:bg-[#f8f7f5]"
            >
              <RotateCcw className="size-3.5" aria-hidden="true" />
              Đặt lại cài đặt
            </button>
          </div>
        </details>
      </div>
    </div>
  )
}

export function WorkspaceSettingsPanel({
  activeTool,
  selectedVoiceId,
  onSelectVoice,
  className,
}: {
  activeTool: SettingsTool
  selectedVoiceId: string
  onSelectVoice: (id: string) => void
  className?: string
}) {
  return (
    <aside aria-label="Cài đặt công cụ" className={cn("motion-panel min-h-0 flex-col", className)}>
      <Tabs defaultValue="settings" className="flex h-full min-h-0 flex-col">
        <TabsList
          variant="line"
          className="mx-4 mt-1 flex h-11 w-auto shrink-0 justify-start gap-5 rounded-none border-b border-[#eceae7] bg-transparent p-0"
        >
          <TabsTrigger value="settings" className="h-11 rounded-none px-1 text-[12px] font-medium">
            Cài đặt
          </TabsTrigger>
          <TabsTrigger value="history" className="h-11 rounded-none px-1 text-[12px] font-medium">
            Lịch sử
          </TabsTrigger>
        </TabsList>

        <TabsContent value="settings" className="min-h-0 flex-1 overflow-y-auto px-4">
          <SettingsContent
            activeTool={activeTool}
            selectedVoiceId={selectedVoiceId}
            onSelectVoice={onSelectVoice}
          />
        </TabsContent>
        <TabsContent value="history" className="min-h-0 flex-1 overflow-y-auto px-4 py-10">
          <div className="mx-auto flex max-w-[230px] flex-col items-center text-center">
            <span className="mb-3 flex size-10 items-center justify-center rounded-xl bg-[#efedff] text-[#675bd0]">
              <AudioLines className="size-4" aria-hidden="true" />
            </span>
            <p className="text-[12px] font-semibold text-[#18181b]">Chưa có lịch sử</p>
            <p className="mt-1 text-[11px] leading-5 text-[#8b8790]">
              Các bản ghi được tạo sẽ xuất hiện tại đây.
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </aside>
  )
}
'''

with open('E:/VoiceAI/extracted_ui_design/components/workspace-settings-panel.tsx', 'w', encoding='utf-8') as f:
    f.write(panel_code)
print("Updated workspace-settings-panel.tsx successfully")
