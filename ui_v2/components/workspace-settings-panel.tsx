"use client"

import { useState, useRef, useEffect } from "react"
import type { CSSProperties } from "react"
import {
  AudioLines,
  Check,
  ChevronDown,
  CircleHelp,
  Download,
  Minus,
  Pause,
  Play,
  RotateCcw,
  Trash2,
  Volume2,
} from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { useVoiceStudio } from "@/components/voice-studio-context"
import {
  defaultVoiceSettings,
  getVoiceById,
  voiceCatalog,
  type HistoryItem,
  type VoiceProfile,
  type VoiceSettings,
} from "@/lib/voice-catalog"
import { cn } from "@/lib/utils"

type SettingsTool = "text-to-speech" | "voice-changer"

type SettingSliderProps = {
  label: string
  lowLabel: string
  highLabel: string
  min: number
  max: number
  step: number
  value: number
  onChange: (value: number) => void
  formatValue: (value: number) => string
}

function SettingSlider({
  label,
  lowLabel,
  highLabel,
  min,
  max,
  step,
  value,
  onChange,
  formatValue,
}: SettingSliderProps) {
  const progress = ((value - min) / (max - min)) * 100

  return (
    <label className="block">
      <span className="flex items-center justify-between gap-2 text-[12px] font-medium text-foreground">
        {label}
        <span className="rounded-md bg-muted px-2 py-1 text-[10px] font-medium tabular-nums text-foreground/80">
          {formatValue(value)}
        </span>
      </span>
      <span className="mt-1.5 flex items-center justify-between gap-3 text-[10px] text-muted-foreground">
        <span>{lowLabel}</span>
        <span className="text-right">{highLabel}</span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        aria-label={label}
        aria-valuetext={formatValue(value)}
        style={{ "--range-progress": `${progress}%` } as CSSProperties}
        className="voice-range mt-2 w-full"
      />
    </label>
  )
}

function SettingSwitch({
  label,
  checked,
  onChange,
}: {
  label: string
  checked: boolean
  onChange: (next: boolean) => void
}) {
  return (
    <div className="flex items-center justify-between gap-3 py-1.5">
      <span className="text-[11px] font-medium leading-4 text-muted-foreground">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        aria-label={label}
        onClick={() => onChange(!checked)}
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
}

function EffectRow({
  title,
  options,
  value,
  onChange,
  onRemove,
}: {
  title: string
  options: string[]
  value: string
  onChange: (val: string) => void
  onRemove: () => void
}) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    if (open) {
      document.addEventListener("mousedown", handleOutside)
    }
    return () => document.removeEventListener("mousedown", handleOutside)
  }, [open])

  return (
    <div ref={containerRef} className="relative flex h-9 items-center rounded-lg border border-border bg-card">
      <span className="flex h-full w-[94px] shrink-0 items-center gap-1.5 border-r border-border px-2 text-[10px] text-muted-foreground">
        <Volume2 className="size-3.5 shrink-0" aria-hidden="true" />
        <span className="whitespace-nowrap">{title}</span>
      </span>
      <button
        type="button"
        aria-label={`${title} effect`}
        aria-expanded={open}
        onClick={() => setOpen((prev) => !prev)}
        className={cn(
          "flex h-full min-w-0 flex-1 items-center justify-between px-2.5 text-left text-[11px] font-medium text-foreground transition-colors outline-none",
          open ? "bg-muted" : "hover:bg-muted/50"
        )}
      >
        <span className="truncate">{value}</span>
        <ChevronDown
          className={cn("size-3.5 shrink-0 text-muted-foreground transition-transform duration-150", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>
      <button
        type="button"
        onClick={onRemove}
        aria-label={`Gỡ hiệu ứng ${title}`}
        className="flex size-8 shrink-0 items-center justify-center border-l border-border text-muted-foreground hover:text-foreground"
      >
        <Minus className="size-3.5" aria-hidden="true" />
      </button>

      {open ? (
        <div
          role="listbox"
          className="absolute left-[94px] right-0 top-[calc(100%+4px)] z-30 rounded-xl border border-border bg-card p-1.5 shadow-lg"
        >
          {options.map((option) => {
            const isSelected = option === value
            return (
              <button
                key={option}
                type="button"
                role="option"
                aria-selected={isSelected}
                onClick={() => {
                  onChange(option)
                  setOpen(false)
                }}
                className={cn(
                  "flex w-full items-center justify-between rounded-lg px-2.5 py-1.5 text-left text-[11px] transition-colors",
                  isSelected
                    ? "bg-primary/10 font-medium text-primary"
                    : "text-foreground hover:bg-muted/60"
                )}
              >
                <span>{option}</span>
                {isSelected ? <Check className="size-3.5 text-primary" aria-hidden="true" /> : null}
              </button>
            )
          })}
        </div>
      ) : null}
    </div>
  )
}

function VoiceOrb({ className }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "block size-9 shrink-0 rounded-full bg-[radial-gradient(circle_at_30%_25%,#f0edff_0%,#a89bf5_34%,#7161d6_68%,#473b91_100%)] shadow-[0_2px_8px_rgba(87,74,170,0.2)]",
        className
      )}
    />
  )
}

function SettingsContent({
  activeTool,
  selectedVoiceId,
  onSelectVoice,
  voices,
  settings,
  onChangeSettings,
}: {
  activeTool: SettingsTool
  selectedVoiceId: string
  onSelectVoice: (id: string) => void
  voices: VoiceProfile[]
  settings: VoiceSettings
  onChangeSettings: (next: VoiceSettings) => void
}) {
  const selectedVoice = getVoiceById(selectedVoiceId, voices)
  const [visibleEffects, setVisibleEffects] = useState(["Distance", "Space"])
  const [playingSample, setPlayingSample] = useState(false)
  const sampleAudioRef = useRef<HTMLAudioElement | null>(null)

  function toggleVoicePreview() {
    const url = selectedVoice.previewUrl || `/api/voices/${selectedVoice.id}/preview`
    if (playingSample && sampleAudioRef.current) {
      sampleAudioRef.current.pause()
      setPlayingSample(false)
      return
    }
    if (sampleAudioRef.current) {
      sampleAudioRef.current.pause()
    }
    const audio = new Audio(url)
    sampleAudioRef.current = audio
    setPlayingSample(true)
    audio.onended = () => setPlayingSample(false)
    audio.onerror = () => setPlayingSample(false)
    audio.play().catch(() => setPlayingSample(false))
  }

  function resetSettings() {
    onChangeSettings(defaultVoiceSettings)
    setVisibleEffects(["Distance", "Space"])
  }

  const isKokoroActive = (settings.engine === "kokoro") || selectedVoice.engine === "kokoro" || selectedVoice.id.startsWith("af_") || selectedVoice.id.startsWith("am_") || selectedVoice.id.startsWith("bf_") || selectedVoice.id.startsWith("bm_")

  return (
    <div className="flex flex-col gap-5 pb-5 pt-4">
      {/* AI ENGINE SELECTOR */}
      <section aria-label="Mô hình AI" className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <label className="text-[12px] font-semibold text-foreground">
            Mô hình AI (Engine)
          </label>
          <span className="rounded-md bg-primary/10 px-1.5 py-0.5 text-[9px] font-semibold text-primary">
            GTX 1650 CUDA
          </span>
        </div>
        <div className="grid grid-cols-2 gap-2 rounded-xl border border-border bg-muted/40 p-1">
          <button
            type="button"
            onClick={() => {
              onChangeSettings({ ...settings, engine: "omnivoice" })
              if (selectedVoice.engine === "kokoro" || selectedVoice.id.startsWith("af_") || selectedVoice.id.startsWith("am_") || selectedVoice.id.startsWith("bf_") || selectedVoice.id.startsWith("bm_")) {
                onSelectVoice("minh-anh")
              }
            }}
            className={cn(
              "flex flex-col items-start gap-0.5 rounded-lg p-2 text-left transition-all",
              !isKokoroActive
                ? "bg-card shadow-xs border border-border/80 text-foreground"
                : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
            )}
          >
            <div className="flex items-center gap-1.5 w-full">
              <span className={cn("size-2 rounded-full", !isKokoroActive ? "bg-emerald-500" : "bg-muted-foreground/40")} />
              <span className="text-[11px] font-bold">OmniVoice FP16</span>
            </div>
            <span className="text-[9.5px] text-muted-foreground line-clamp-1">Đa ngôn ngữ & Tiếng Việt</span>
          </button>

          <button
            type="button"
            onClick={() => {
              onChangeSettings({ ...settings, engine: "kokoro" })
              if (selectedVoice.id === "minh-anh" || selectedVoice.id === "bao-ngoc" || selectedVoice.id === "gia-huy") {
                onSelectVoice("af_heart")
              }
            }}
            className={cn(
              "flex flex-col items-start gap-0.5 rounded-lg p-2 text-left transition-all",
              isKokoroActive
                ? "bg-card shadow-xs border border-border/80 text-foreground"
                : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
            )}
          >
            <div className="flex items-center gap-1.5 w-full">
              <span className={cn("size-2 rounded-full", isKokoroActive ? "bg-cyan-500" : "bg-muted-foreground/40")} />
              <span className="text-[11px] font-bold">Kokoro-82M</span>
            </div>
            <span className="text-[9.5px] text-muted-foreground line-clamp-1">Siêu tốc 0.5s & US/UK Hi-Fi</span>
          </button>
        </div>
      </section>

      {/* VOICE SELECTOR */}
      <section aria-label="Chọn giọng đọc" className="flex flex-col gap-2.5">
        <label htmlFor="settings-voice" className="text-[12px] font-semibold text-foreground">
          Giọng đọc
        </label>
        <span className="relative block">
          <select
            id="settings-voice"
            value={selectedVoice.id}
            onChange={(event) => {
              const vid = event.target.value
              onSelectVoice(vid)
              const v = voices.find((item) => item.id === vid)
              if (v?.engine === "kokoro" || vid.startsWith("af_") || vid.startsWith("am_") || vid.startsWith("bf_") || vid.startsWith("bm_")) {
                onChangeSettings({ ...settings, engine: "kokoro" })
              } else if (v?.engine === "omnivoice" || vid === "minh-anh" || vid === "bao-ngoc" || vid === "gia-huy") {
                onChangeSettings({ ...settings, engine: "omnivoice" })
              }
            }}
            className="h-10 w-full appearance-none rounded-xl border border-border bg-card pl-3 pr-9 text-[11px] text-foreground outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
          >
            <optgroup label="⚡ Kokoro-82M (Siêu tốc 0.5s · US/UK Hi-Fi)">
              {voices
                .filter((v) => v.engine === "kokoro" || v.id.startsWith("af_") || v.id.startsWith("am_") || v.id.startsWith("bf_") || v.id.startsWith("bm_"))
                .map((voice) => (
                  <option key={voice.id} value={voice.id}>{`${voice.name} — ${voice.style}`}</option>
                ))}
            </optgroup>
            <optgroup label="🇻🇳 OmniVoice (Đa ngôn ngữ & Tiếng Việt)">
              {voices
                .filter((v) => !(v.engine === "kokoro" || v.id.startsWith("af_") || v.id.startsWith("am_") || v.id.startsWith("bf_") || v.id.startsWith("bm_")))
                .map((voice) => (
                  <option key={voice.id} value={voice.id}>{`${voice.name} — ${voice.style}`}</option>
                ))}
            </optgroup>
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
        </span>
        <div className="flex items-center gap-3 rounded-xl bg-muted/40 p-3">
          <button
            type="button"
            onClick={toggleVoicePreview}
            title={`Nghe thử giọng ${selectedVoice.name}`}
            aria-label={`Nghe thử giọng ${selectedVoice.name}`}
            className="group relative shrink-0 rounded-full focus:outline-none"
          >
            <VoiceOrb />
            <span className="absolute inset-0 flex items-center justify-center rounded-full bg-black/25 text-white opacity-0 transition-opacity group-hover:opacity-100">
              {playingSample ? <Pause className="size-3.5 fill-current" /> : <Play className="ml-0.5 size-3.5 fill-current" />}
            </span>
          </button>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5">
              <p className="truncate text-[11px] font-semibold text-foreground">
                {selectedVoice.name} · {selectedVoice.locale} · {selectedVoice.gender}
              </p>
              <span className={cn(
                "rounded px-1.5 py-0.5 text-[9px] font-semibold",
                isKokoroActive
                  ? "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400"
                  : "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
              )}>
                {isKokoroActive ? "Kokoro-82M" : "OmniVoice"}
              </span>
            </div>
            <p className="mt-0.5 truncate text-[10px] text-muted-foreground">{selectedVoice.description}</p>
            <p className="mt-1 text-[10px] text-muted-foreground">
              {activeTool === "voice-changer" ? "Giọng đích cho tệp âm thanh" : "Giọng dùng cho kịch bản"}
            </p>
          </div>
        </div>
      </section>

      <div className="flex flex-col gap-4">
        <SettingSlider
          label="Tốc độ đọc"
          lowLabel="Chậm hơn"
          highLabel="Nhanh hơn"
          min={0.7}
          max={1.4}
          step={0.05}
          value={settings.speed}
          onChange={(speed) => onChangeSettings({ ...settings, speed })}
          formatValue={(value) => `${value.toFixed(2)}x`}
        />

        <details open className="motion-disclosure group rounded-xl border border-border bg-card p-3">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-3 text-[12px] font-semibold text-foreground">
            Tùy chỉnh nâng cao
            <ChevronDown className="size-4 text-muted-foreground transition-transform group-open:rotate-180" aria-hidden="true" />
          </summary>
          <div className="mt-4 flex flex-col gap-4">
            <SettingSlider
              label="Độ ổn định"
              lowLabel="Linh hoạt"
              highLabel="Ổn định"
              min={0}
              max={100}
              step={5}
              value={settings.stability}
              onChange={(stability) => onChangeSettings({ ...settings, stability })}
              formatValue={(value) => `${value}%`}
            />
            <SettingSlider
              label="Độ bám giọng mẫu"
              lowLabel="Linh hoạt"
              highLabel="Giống mẫu"
              min={0}
              max={100}
              step={5}
              value={settings.similarity}
              onChange={(similarity) => onChangeSettings({ ...settings, similarity })}
              formatValue={(value) => `${value}%`}
            />
            <SettingSlider
              label="Nhấn nhá cảm xúc"
              lowLabel="Tự nhiên"
              highLabel="Kịch tính"
              min={0}
              max={100}
              step={5}
              value={settings.style}
              onChange={(style) => onChangeSettings({ ...settings, style })}
              formatValue={(value) => `${value}%`}
            />

            <details open className="motion-disclosure border-t border-border pt-3">
              <summary className="flex cursor-pointer list-none items-center justify-between text-[11px] font-semibold text-muted-foreground">
                Hiệu ứng âm thanh
                <ChevronDown className="size-4 text-muted-foreground" aria-hidden="true" />
              </summary>
              <div className="mt-3 flex flex-col gap-2">
                {visibleEffects.includes("Distance") ? (
                  <EffectRow
                    title="Khoảng cách"
                    options={["Gần", "Vừa", "Xa"]}
                    value={settings.distance}
                    onChange={(distance) => onChangeSettings({ ...settings, distance })}
                    onRemove={() => {
                      setVisibleEffects((current) => current.filter((effect) => effect !== "Distance"))
                      onChangeSettings({ ...settings, distance: "Vừa" })
                    }}
                  />
                ) : null}
                {visibleEffects.includes("Space") ? (
                  <EffectRow
                    title="Không gian"
                    options={["Phòng thu khô", "Phòng nhỏ", "Sảnh lớn", "Điện thoại"]}
                    value={settings.space}
                    onChange={(space) => onChangeSettings({ ...settings, space })}
                    onRemove={() => {
                      setVisibleEffects((current) => current.filter((effect) => effect !== "Space"))
                      onChangeSettings({ ...settings, space: "Phòng thu khô" })
                    }}
                  />
                ) : null}
              </div>
              {visibleEffects.length === 0 ? (
                <button
                  type="button"
                  onClick={() => {
                    setVisibleEffects(["Distance", "Space"])
                    onChangeSettings({ ...settings, distance: "Xa", space: "Phòng thu khô" })
                  }}
                  className="mt-2 text-[10px] font-medium text-primary underline underline-offset-2"
                >
                  Thêm lại hiệu ứng
                </button>
              ) : null}
            </details>

            <div className="border-t border-border pt-3">
              <label className="flex items-center justify-between gap-3">
                <span className="text-[11px] font-medium text-muted-foreground">Ngôn ngữ</span>
                <select
                  value={settings.language}
                  onChange={(e) => onChangeSettings({ ...settings, language: e.target.value })}
                  className="h-8 max-w-[140px] rounded-lg border border-border bg-card px-2 text-[10px] text-foreground outline-none focus:border-primary"
                >
                  <option>English</option>
                  <option>Tiếng Việt</option>
                  <option>Tự động</option>
                </select>
              </label>
              <div className="mt-2">
                <SettingSwitch
                  label="Chuẩn âm lượng phòng thu (-14 LUFS)"
                  checked={settings.lufs}
                  onChange={(lufs) => onChangeSettings({ ...settings, lufs })}
                />
              </div>
              <div className="mt-1">
                <SettingSwitch
                  label="Giảm tiếng ồn nền"
                  checked={settings.denoise}
                  onChange={(denoise) => onChangeSettings({ ...settings, denoise })}
                />
              </div>
              <label className="mt-3 flex flex-col gap-1.5">
                <span className="text-[11px] font-medium text-muted-foreground">Định dạng đầu ra</span>
                <select
                  value={settings.format}
                  onChange={(e) => onChangeSettings({ ...settings, format: e.target.value })}
                  className="h-9 w-full rounded-lg border border-border bg-card px-2.5 text-[10px] text-foreground outline-none focus:border-primary"
                >
                  <option>WAV · 24 kHz</option>
                  <option>MP3 · 44.1 kHz · 128 kbps</option>
                  <option>WAV · 48 kHz</option>
                </select>
              </label>
            </div>

            <button
              type="button"
              onClick={resetSettings}
              className="flex h-9 items-center justify-center gap-1.5 rounded-lg border border-border text-[11px] font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            >
              <RotateCcw className="size-3.5" aria-hidden="true" />
              Đặt lại cài đặt
            </button>
            <p className="flex items-start gap-1.5 text-[10px] leading-4 text-muted-foreground">
              <CircleHelp className="mt-0.5 size-3.5 shrink-0" aria-hidden="true" />
              Đã kết nối bộ máy âm thanh GPU OmniVoice FP16 (24 kHz).
            </p>
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
  voices = voiceCatalog,
  settings = defaultVoiceSettings,
  onChangeSettings = () => {},
  history = [],
  className,
}: {
  activeTool: SettingsTool
  selectedVoiceId: string
  onSelectVoice: (id: string) => void
  voices?: VoiceProfile[]
  settings?: VoiceSettings
  onChangeSettings?: (next: VoiceSettings) => void
  history?: HistoryItem[]
  className?: string
}) {
  const { deleteHistoryItem, clearAllHistory } = useVoiceStudio()

  return (
    <aside aria-label="Cài đặt công cụ" className={cn("motion-panel min-h-0 flex-col", className)}>
      <Tabs defaultValue="settings" className="flex h-full min-h-0 flex-col">
        <TabsList
          variant="line"
          className="mx-4 mt-1 flex h-11 w-auto shrink-0 justify-start gap-5 rounded-none border-b border-border bg-transparent p-0"
        >
          <TabsTrigger value="settings" className="h-11 rounded-none px-1 text-[12px] font-medium">
            Cài đặt
          </TabsTrigger>
          <TabsTrigger value="history" className="h-11 rounded-none px-1 text-[12px] font-medium">
            Lịch sử {history.length > 0 ? `(${history.length})` : ""}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="settings" className="min-h-0 flex-1 overflow-y-auto px-4">
          <SettingsContent
            activeTool={activeTool}
            selectedVoiceId={selectedVoiceId}
            onSelectVoice={onSelectVoice}
            voices={voices}
            settings={settings}
            onChangeSettings={onChangeSettings}
          />
        </TabsContent>
        <TabsContent value="history" className="min-h-0 flex-1 overflow-y-auto px-4 py-4">
          {history.length === 0 ? (
            <div className="mx-auto flex max-w-[230px] flex-col items-center py-6 text-center">
              <span className="mb-3 flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <AudioLines className="size-4" aria-hidden="true" />
              </span>
              <p className="text-[12px] font-semibold text-foreground">Chưa có lịch sử</p>
              <p className="mt-1 text-[11px] leading-5 text-muted-foreground">
                Các bản ghi được tạo sẽ xuất hiện tại đây.
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-2.5">
              <div className="flex items-center justify-between pb-1">
                <span className="text-[11px] font-semibold text-muted-foreground">
                  Bản ghi đã lưu ({history.length})
                </span>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => clearAllHistory()}
                  className="h-7 gap-1 px-2 text-[11px] text-destructive hover:bg-destructive/10 hover:text-destructive"
                >
                  <Trash2 className="size-3" />
                  Dọn sạch
                </Button>
              </div>

              {history.map((item) => (
                <div
                  key={item.filename}
                  className="group flex flex-col gap-2 rounded-xl border border-border bg-card p-2.5 shadow-2xs transition-colors hover:border-primary/20"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate text-[11px] font-semibold text-foreground" title={item.filename}>
                      {item.filename}
                    </span>
                    <div className="flex items-center gap-1">
                      <a
                        href={item.audioUrl}
                        download={item.filename}
                        title="Tải xuống WAV"
                        className="flex size-6 shrink-0 items-center justify-center rounded-md text-primary transition-colors hover:bg-primary/10"
                      >
                        <Download className="size-3.5" />
                      </a>
                      <button
                        type="button"
                        onClick={() => deleteHistoryItem(item.filename)}
                        title="Xóa bản ghi này"
                        aria-label={`Xóa bản ghi ${item.filename}`}
                        className="flex size-6 shrink-0 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
                      >
                        <Trash2 className="size-3.5" />
                      </button>
                    </div>
                  </div>
                  <span className="text-[10px] text-muted-foreground">
                    {item.createdAt} · {item.sizeKb} KB
                  </span>
                  <audio controls src={item.audioUrl} className="h-8 w-full" />
                </div>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </aside>
  )
}
