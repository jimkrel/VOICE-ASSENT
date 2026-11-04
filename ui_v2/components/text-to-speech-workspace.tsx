"use client"

import { useEffect, useId, useMemo, useRef, useState } from "react"
import {
  Check,
  CheckCircle2,
  ChevronDown,
  CloudRain,
  Drama,
  Flame,
  Globe2,
  Leaf,
  Loader2,
  Play,
  RotateCcw,
  Smile,
  Sparkles,
  Trash2,
  Volume2,
  Wind,
  X,
} from "lucide-react"
import type { LucideIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { StudioWaveformPlayer, type StudioLogItem } from "@/components/studio-waveform-player"
import {
  defaultVoiceSettings,
  getVoiceById,
  voiceCatalog,
  type VoiceProfile,
  type VoiceSettings,
} from "@/lib/voice-catalog"
import { cn } from "@/lib/utils"

const initialScript = `[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.\n[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.\n[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số.\n[điềm tĩnh] Cảm ơn bạn đã lắng nghe.`

const emotionOptions: { label: string; tag: string; icon: LucideIcon }[] = [
  { label: "Kịch tính", tag: "[kịch tính]", icon: Drama },
  { label: "Thì thầm", tag: "[thì thầm]", icon: Wind },
  { label: "Hào hứng", tag: "[hào hứng]", icon: Flame },
  { label: "Buồn bã", tag: "[buồn]", icon: CloudRain },
  { label: "Tức giận", tag: "[tức giận]", icon: Sparkles },
  { label: "Thở dài", tag: "[thở dài]", icon: Wind },
  { label: "Điềm tĩnh", tag: "[điềm tĩnh]", icon: Leaf },
]

type TTSResult = {
  audioUrl: string
  filename: string
  voiceName: string
  duration: number
  elapsed: number
  chunks: number
  steps: number
  emotions: string[]
  distance: string
  space: string
  createdAt: string
  waveform?: number[]
  logs?: StudioLogItem[]
}

const VI_CHAR_REGEX = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i

export function TextToSpeechWorkspace({
  selectedVoiceId = "minh-anh",
  onSelectVoice,
  voices = voiceCatalog,
  settings = defaultVoiceSettings,
  onChangeSettings,
  onGenerated,
}: {
  selectedVoiceId?: string
  onSelectVoice?: (id: string) => void
  voices?: VoiceProfile[]
  settings?: VoiceSettings
  onChangeSettings?: (s: VoiceSettings) => void
  onGenerated?: () => void
}) {
  const [text, setText] = useState(initialScript)
  const [notice, setNotice] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [progressPct, setProgressPct] = useState(0)
  const [result, setResult] = useState<TTSResult | null>(null)
  const [countdown, setCountdown] = useState<number | null>(null)
  const [voiceDropdownOpen, setVoiceDropdownOpen] = useState(false)
  const [playingPreview, setPlayingPreview] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const previewAudioRef = useRef<HTMLAudioElement | null>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const activeCatalog = voices && voices.length > 0 ? voices : voiceCatalog
  const currentVoice = useMemo(
    () => getVoiceById(selectedVoiceId, activeCatalog),
    [selectedVoiceId, activeCatalog]
  )

  const isVietnameseText = useMemo(() => VI_CHAR_REGEX.test(text), [text])

  // Suggested popular voices
  const quickVoices = useMemo(() => {
    const viList = activeCatalog.filter(
      (v) =>
        v.language?.toLowerCase().includes("việt") ||
        v.categories?.some((c) => c.toLowerCase().includes("việt"))
    )
    const enList = activeCatalog.filter(
      (v) =>
        v.language?.toLowerCase().includes("english") ||
        v.categories?.some((c) => c.toLowerCase().includes("english"))
    )
    return [...viList.slice(0, 3), ...enList.slice(0, 2)]
  }, [activeCatalog])

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setVoiceDropdownOpen(false)
      }
    }
    if (voiceDropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside)
      return () => document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [voiceDropdownOpen])

  useEffect(() => {
    if (!isGenerating) return
    setProgressPct(8)
    const timer = setInterval(() => {
      setProgressPct((prev) => (prev < 92 ? prev + Math.max(1, Math.round((92 - prev) * 0.14)) : prev))
    }, 450)
    return () => clearInterval(timer)
  }, [isGenerating])

  useEffect(() => {
    if (countdown === null) return
    if (countdown <= 0) {
      setNotice("")
      setCountdown(null)
      return
    }
    const timer = setTimeout(() => setCountdown((c) => (c !== null ? c - 1 : null)), 1000)
    return () => clearTimeout(timer)
  }, [countdown])

  function togglePreview(voice: VoiceProfile) {
    const url = voice.previewUrl || `/api/voices/${voice.id}/preview`
    if (playingPreview && previewAudioRef.current) {
      previewAudioRef.current.pause()
      setPlayingPreview(false)
      return
    }
    if (previewAudioRef.current) {
      previewAudioRef.current.pause()
    }
    const audio = new Audio(url)
    previewAudioRef.current = audio
    setPlayingPreview(true)
    audio.onended = () => setPlayingPreview(false)
    audio.onerror = () => setPlayingPreview(false)
    audio.play().catch(() => setPlayingPreview(false))
  }

  function handleSelectVoice(vId: string) {
    onSelectVoice?.(vId)
    setVoiceDropdownOpen(false)
  }

  function insertTag(tag: string) {
    const textarea = textareaRef.current
    if (!textarea) return

    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const prefix = start > 0 && !/[\s\n]$/.test(text.slice(0, start)) ? " " : ""
    const suffix = " "
    const nextText = `${text.slice(0, start)}${prefix}${tag}${suffix}${text.slice(end)}`
    const nextPosition = start + prefix.length + tag.length + suffix.length

    setText(nextText)
    setNotice("")
    setErrorMsg("")
    requestAnimationFrame(() => {
      textarea.focus()
      textarea.setSelectionRange(nextPosition, nextPosition)
    })
  }

  async function handleGenerate() {
    const textToSubmit = (textareaRef.current?.value ?? text).trim()
    if (!textToSubmit || isGenerating) return

    // If Vietnamese text and selected voice is English "hope", automatically select Minh Anh
    let effectiveVoiceId = selectedVoiceId
    if ((!effectiveVoiceId || effectiveVoiceId === "hope") && isVietnameseText) {
      effectiveVoiceId = "minh-anh"
      onSelectVoice?.("minh-anh")
    }

    const targetLang =
      settings.language === "Tự động"
        ? isVietnameseText
          ? "Tiếng Việt"
          : "English"
        : settings.language

    setIsGenerating(true)
    setErrorMsg("")
    setProgressPct(8)
    setNotice("Đang nạp kịch bản vào GPU NVIDIA GeForce GTX 1650...")
    setCountdown(null)

    const startTime = Date.now()
    const timer = setInterval(() => {
      const elapsedSec = ((Date.now() - startTime) / 1000).toFixed(1)
      setProgressPct((prev) => Math.min(92, Math.round(prev + (92 - prev) * 0.12)))
      setNotice(`Đang tổng hợp trên GPU GTX 1650 (${elapsedSec}s)...`)
    }, 400)

    try {
      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: textToSubmit,
          voiceId: effectiveVoiceId,
          ...settings,
          language: targetLang,
        }),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || "Không thể tạo giọng đọc.")
      }
      clearInterval(timer)
      setProgressPct(100)
      setResult(data)
      setNotice(
        `Đã tạo giọng thành công (${data.voiceName}) · ${data.duration}s âm thanh trong ${data.elapsed}s · ${data.chunks} phân đoạn`
      )
      setCountdown(10)
      onGenerated?.()
    } catch (err: unknown) {
      clearInterval(timer)
      const msg = err instanceof Error ? err.message : "Lỗi kết nối tới máy chủ âm thanh."
      setErrorMsg(msg)
      setNotice("")
      setProgressPct(0)
    } finally {
      clearInterval(timer)
      setIsGenerating(false)
    }
  }

  function handleClear() {
    setText("")
    setNotice("")
    setErrorMsg("")
    setCountdown(null)
    textareaRef.current?.focus()
  }

  function restoreSample() {
    setText(initialScript)
    setNotice("")
    setErrorMsg("")
    setCountdown(null)
  }

  const badges = result
    ? [
        `Giọng: ${result.voiceName}`,
        `Khoảng cách: ${result.distance}`,
        `Không gian: ${result.space}`,
        ...(result.emotions || []).map((e) => `Sắc thái: ${e}`),
      ]
    : []

  return (
    <section className="motion-screen min-h-full px-4 py-5 sm:px-6 sm:py-6" aria-label="Đọc kịch bản">
      <div className="mx-auto flex w-full max-w-[960px] flex-col gap-4">
        {/* Header */}
        <header>
          <h2 className="text-[22px] font-semibold tracking-[-0.04em] text-foreground sm:text-[24px]">
            Biến kịch bản thành giọng đọc
          </h2>
          <p className="mt-1 max-w-[640px] text-[12px] leading-5 text-muted-foreground">
            Dán nội dung, chọn giọng đọc tiếng Việt hoặc tiếng Anh và xuất âm thanh chuẩn studio 24 kHz.
          </p>
        </header>

        {/* VOICE & LANGUAGE BAR - DIRECT ACCESS */}
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-border bg-card p-3 shadow-xs sm:px-4 sm:py-3">
          <div className="flex min-w-0 flex-1 items-center gap-3">
            {/* Custom Voice Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <button
                type="button"
                onClick={() => setVoiceDropdownOpen(!voiceDropdownOpen)}
                className="flex items-center gap-2.5 rounded-xl border border-border bg-muted/30 px-3 py-2 text-left transition-colors hover:border-primary/40 hover:bg-primary/5 focus:outline-none focus:ring-2 focus:ring-primary/20"
                aria-haspopup="listbox"
                aria-expanded={voiceDropdownOpen}
              >
                <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-linear-to-tr from-primary to-primary/70 text-[11px] font-bold text-primary-foreground shadow-xs">
                  {currentVoice.name.slice(0, 2).toUpperCase()}
                </span>
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="truncate text-[12px] font-semibold text-foreground">
                      {currentVoice.name}
                    </span>
                    <span className="rounded bg-primary/10 px-1.5 py-0.5 text-[9px] font-semibold text-primary">
                      {currentVoice.language?.includes("Việt") ? "🇻🇳 Tiếng Việt" : "🇺🇸 English"}
                    </span>
                  </div>
                  <p className="truncate text-[10px] text-muted-foreground">
                    {currentVoice.gender} · {currentVoice.style}
                  </p>
                </div>
                <ChevronDown className="ml-1 size-4 text-muted-foreground" />
              </button>

              {/* Dropdown Menu */}
              {voiceDropdownOpen ? (
                <div className="absolute left-0 top-full z-50 mt-1 max-h-[320px] w-[280px] overflow-y-auto rounded-xl border border-border bg-card p-1.5 shadow-xl sm:w-[320px]">
                  <div className="px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    Giọng Tiếng Việt Khuyến Nghị
                  </div>
                  {activeCatalog
                    .filter(
                      (v) =>
                        v.language?.toLowerCase().includes("việt") ||
                        v.categories?.some((c) => c.toLowerCase().includes("việt"))
                    )
                    .map((voice) => {
                      const isSelected = voice.id === selectedVoiceId
                      return (
                        <button
                          key={voice.id}
                          type="button"
                          onClick={() => handleSelectVoice(voice.id)}
                          className={cn(
                            "flex w-full items-center justify-between rounded-lg px-2.5 py-2 text-left transition-colors",
                            isSelected
                              ? "bg-primary/10 font-medium text-primary"
                              : "text-foreground hover:bg-muted/60"
                          )}
                        >
                          <div className="min-w-0">
                            <div className="flex items-center gap-1.5">
                              <span className="text-[12px] font-semibold">{voice.name}</span>
                              <span className="text-[10px] text-muted-foreground">({voice.gender})</span>
                            </div>
                            <p className="truncate text-[10px] text-muted-foreground">{voice.description}</p>
                          </div>
                          {isSelected ? <Check className="size-4 shrink-0 text-primary" /> : null}
                        </button>
                      )
                    })}

                  <div className="mt-2 border-t border-border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    Giọng Quốc Tế (English)
                  </div>
                  {activeCatalog
                    .filter(
                      (v) =>
                        !v.language?.toLowerCase().includes("việt") &&
                        !v.categories?.some((c) => c.toLowerCase().includes("việt"))
                    )
                    .slice(0, 8)
                    .map((voice) => {
                      const isSelected = voice.id === selectedVoiceId
                      return (
                        <button
                          key={voice.id}
                          type="button"
                          onClick={() => handleSelectVoice(voice.id)}
                          className={cn(
                            "flex w-full items-center justify-between rounded-lg px-2.5 py-2 text-left transition-colors",
                            isSelected
                              ? "bg-primary/10 font-medium text-primary"
                              : "text-foreground hover:bg-muted/60"
                          )}
                        >
                          <div className="min-w-0">
                            <div className="flex items-center gap-1.5">
                              <span className="text-[12px] font-semibold">{voice.name}</span>
                              <span className="text-[10px] text-muted-foreground">({voice.locale || "US"})</span>
                            </div>
                            <p className="truncate text-[10px] text-muted-foreground">{voice.description}</p>
                          </div>
                          {isSelected ? <Check className="size-4 shrink-0 text-primary" /> : null}
                        </button>
                      )
                    })}
                </div>
              ) : null}
            </div>

            {/* Quick Voice Chips */}
            <div className="hidden items-center gap-1.5 xl:flex">
              {quickVoices.map((v) => {
                const isActive = v.id === selectedVoiceId
                return (
                  <button
                    key={v.id}
                    type="button"
                    onClick={() => handleSelectVoice(v.id)}
                    className={cn(
                      "rounded-lg px-2.5 py-1 text-[11px] font-medium transition-colors",
                      isActive
                        ? "bg-primary text-primary-foreground shadow-xs"
                        : "bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                    )}
                  >
                    {v.name}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Preview & Status */}
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => togglePreview(currentVoice)}
              className="h-8 gap-1.5 rounded-lg border-border px-2.5 text-[11px] font-medium"
            >
              <Volume2 className={cn("size-3.5", playingPreview ? "animate-pulse text-primary" : "")} />
              <span>{playingPreview ? "Dừng thử" : "Nghe thử giọng"}</span>
            </Button>

            {/* Language auto-detect pill */}
            <div className="flex items-center gap-1.5 rounded-lg border border-border bg-muted/40 px-2.5 py-1 text-[11px] text-muted-foreground">
              <Globe2 className="size-3.5 text-primary" />
              <span className="font-medium text-foreground">
                {isVietnameseText ? "🇻🇳 Tiếng Việt" : "Tự động"}
              </span>
            </div>
          </div>
        </div>

        {/* Emotion Tags Bar */}
        <div className="flex min-w-0 items-center gap-3 rounded-xl border border-border bg-card px-3 py-2.5 shadow-xs">
          <div className="flex shrink-0 items-center gap-1.5 text-[11px] font-semibold text-foreground">
            <Smile className="size-4 text-primary" aria-hidden="true" />
            <span>Sắc thái</span>
          </div>
          <div className="flex min-w-0 flex-1 gap-1.5 overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            {emotionOptions.map((option) => {
              const Icon = option.icon
              return (
                <Button
                  key={option.tag}
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => insertTag(option.tag)}
                  className="h-8 shrink-0 gap-1.5 rounded-lg border-border bg-card px-2.5 text-[11px] font-medium text-muted-foreground hover:bg-muted hover:text-foreground"
                >
                  <Icon data-icon="inline-start" />
                  {option.label}
                </Button>
              )
            })}
          </div>
        </div>

        {/* Textarea Container */}
        <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-xs focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20">
          <label htmlFor="script-input" className="sr-only">
            Kịch bản cần chuyển thành giọng nói
          </label>
          <textarea
            ref={textareaRef}
            id="script-input"
            value={text}
            maxLength={5000}
            onChange={(event) => {
              setText(event.target.value)
              setNotice("")
              setErrorMsg("")
            }}
            onPaste={(event) => {
              const pasted = event.clipboardData.getData("text")
              if (pasted) {
                setNotice("")
                setErrorMsg("")
              }
            }}
            placeholder="Nhập hoặc dán kịch bản tiếng Việt hoặc tiếng Anh vào đây..."
            className="min-h-[260px] w-full resize-y bg-transparent px-4 py-4 text-[13px] leading-6 text-foreground outline-none placeholder:text-muted-foreground sm:min-h-[260px] sm:px-5 sm:py-5 sm:text-[14px]"
          />
          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border px-3.5 py-2.5 sm:px-5">
            <div className="flex items-center gap-3">
              <span className="text-[11px] tabular-nums text-muted-foreground">
                {text.length.toLocaleString("vi-VN")} / 5.000 ký tự
              </span>
              {isVietnameseText ? (
                <span className="rounded bg-primary/10 px-2 py-0.5 text-[10px] font-medium text-primary">
                  ✓ Kịch bản tiếng Việt
                </span>
              ) : null}
            </div>
            <div className="ml-auto flex flex-wrap items-center justify-end gap-1.5">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={handleClear}
                disabled={!text || isGenerating}
                className="h-8 rounded-lg px-2.5 text-[11px] font-medium text-muted-foreground hover:bg-muted"
              >
                <Trash2 data-icon="inline-start" />
                Xóa
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={restoreSample}
                disabled={isGenerating}
                className="h-8 rounded-lg px-2.5 text-[11px] font-medium text-muted-foreground hover:bg-muted"
              >
                <RotateCcw data-icon="inline-start" />
                Mẫu
              </Button>
              <Button
                type="button"
                onClick={handleGenerate}
                disabled={!text.trim() || isGenerating}
                className="h-9 rounded-lg bg-primary px-4 text-[12px] font-semibold text-primary-foreground shadow-xs hover:bg-primary/90"
              >
                {isGenerating ? (
                  <Loader2 className="size-3.5 animate-spin" data-icon="inline-start" />
                ) : (
                  <Play data-icon="inline-start" />
                )}
                {isGenerating ? `Đang tạo (${progressPct}%)` : "Tạo giọng đọc"}
              </Button>
            </div>
          </div>
          {isGenerating ? (
            <div className="h-1 w-full bg-primary/20">
              <div
                className="h-full bg-primary transition-all duration-300"
                style={{ width: `${progressPct}%` }}
              />
            </div>
          ) : null}
        </div>

        {errorMsg ? (
          <p role="alert" className="rounded-xl border border-destructive/20 bg-destructive/10 px-3.5 py-2.5 text-[11px] leading-5 text-destructive">
            {errorMsg}
          </p>
        ) : null}

        {notice ? (
          <div
            role="status"
            className="flex items-center justify-between gap-3 rounded-xl border border-primary/20 bg-primary/5 px-3.5 py-2.5 text-[11px] leading-5 text-primary"
          >
            <span className="flex items-center gap-2">
              {isGenerating ? (
                <Loader2 className="size-3.5 shrink-0 animate-spin text-primary" />
              ) : (
                <CheckCircle2 className="size-3.5 shrink-0 text-primary" />
              )}
              <span>{notice}</span>
            </span>
            {countdown !== null ? (
              <span className="flex shrink-0 items-center gap-1.5">
                <span className="rounded-md bg-primary/10 px-1.5 py-0.5 text-[10px] font-semibold tabular-nums text-primary">
                  {countdown}s
                </span>
                <button
                  type="button"
                  onClick={() => {
                    setNotice("")
                    setCountdown(null)
                  }}
                  aria-label="Đóng thông báo"
                  className="text-muted-foreground hover:text-foreground"
                >
                  <X className="size-3.5" />
                </button>
              </span>
            ) : null}
          </div>
        ) : null}

        <StudioWaveformPlayer
          title="Bản ghi Studio (24 kHz WAV)"
          audioUrl={result?.audioUrl}
          filename={result?.filename}
          duration={result?.duration}
          elapsed={result?.elapsed}
          waveform={result?.waveform}
          logs={result?.logs}
          badges={badges}
          emptyTitle="Chưa có bản ghi nào"
          emptyDescription="Nhập hoặc dán kịch bản, chọn giọng đọc và nhấn “Tạo giọng đọc” để xuất âm thanh."
        />
      </div>
    </section>
  )
}
