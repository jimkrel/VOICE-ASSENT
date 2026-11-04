"use client"

import { useEffect, useMemo, useRef, useState, type DragEvent } from "react"
import {
  AudioLines,
  Check,
  ChevronDown,
  Globe2,
  Loader2,
  Sparkles,
  Upload,
  Volume2,
  X,
} from "lucide-react"
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

type SelectedFile = {
  name: string
  size: number
  file: File
}

type ChangerResult = {
  audioUrl: string
  filename: string
  voiceName: string
  duration: number
  elapsed: number
  waveform?: number[]
  logs?: StudioLogItem[]
}

const MAX_FILE_SIZE = 50 * 1024 * 1024

function formatFileSize(size: number) {
  return size < 1024 * 1024
    ? `${Math.max(1, Math.round(size / 1024))} KB`
    : `${(size / (1024 * 1024)).toFixed(1)} MB`
}

export function VoiceChangerWorkspace({
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
  const [selectedFile, setSelectedFile] = useState<SelectedFile | null>(null)
  const [fileError, setFileError] = useState("")
  const [notice, setNotice] = useState("")
  const [prompt, setPrompt] = useState("")
  const [isDragging, setIsDragging] = useState(false)
  const [isConverting, setIsConverting] = useState(false)
  const [result, setResult] = useState<ChangerResult | null>(null)
  const [voiceDropdownOpen, setVoiceDropdownOpen] = useState(false)
  const [playingPreview, setPlayingPreview] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const previewAudioRef = useRef<HTMLAudioElement | null>(null)

  const activeCatalog = voices && voices.length > 0 ? voices : voiceCatalog
  const currentVoice = useMemo(
    () => getVoiceById(selectedVoiceId, activeCatalog),
    [selectedVoiceId, activeCatalog]
  )

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

  function acceptFile(file?: File) {
    if (!file) return

    if (file.size > MAX_FILE_SIZE) {
      setSelectedFile(null)
      setFileError("Mỗi tệp cần có dung lượng dưới 50 MB.")
      setNotice("")
      return
    }

    const isSupportedType =
      file.type.startsWith("audio/") ||
      file.type.startsWith("video/") ||
      /\.(mp3|wav|m4a|aac|ogg|mp4|mov|webm)$/i.test(file.name)

    if (!isSupportedType) {
      setSelectedFile(null)
      setFileError("Vui lòng chọn tệp âm thanh hoặc video được hỗ trợ (MP3, WAV, M4A, MP4).")
      setNotice("")
      return
    }

    setSelectedFile({ name: file.name, size: file.size, file })
    setFileError("")
    setNotice("")
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault()
    setIsDragging(false)
    acceptFile(event.dataTransfer.files[0])
  }

  async function handleConvert() {
    if (!selectedFile || isConverting) return
    setIsConverting(true)
    setFileError("")
    setNotice("Đang tải dữ liệu âm thanh và nạp vào GPU NVIDIA GeForce GTX 1650...")
    const startTime = Date.now()
    const timer = setInterval(() => {
      const elapsedSec = ((Date.now() - startTime) / 1000).toFixed(1)
      setNotice(`Đang chuyển đổi âm sắc sang giọng ${currentVoice.name} trên GPU (${elapsedSec}s)...`)
    }, 400)
    try {
      const fd = new FormData()
      fd.append("file", selectedFile.file)
      fd.append("voiceId", selectedVoiceId)
      fd.append("prompt", prompt.trim())
      fd.append("speed", String(settings.speed))
      fd.append("stability", String(settings.stability))
      fd.append("similarity", String(settings.similarity))
      fd.append("distance", settings.distance)
      fd.append("space", settings.space)
      fd.append("language", settings.language)
      fd.append("lufs", String(settings.lufs))

      const res = await fetch("/api/changer", {
        method: "POST",
        body: fd,
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || "Không thể chuyển đổi giọng nói.")
      }
      clearInterval(timer)
      setResult(data)
      setNotice(`Đã đổi sang giọng “${data.voiceName}” thành công (${data.duration}s trong ${data.elapsed}s)!`)
      onGenerated?.()
    } catch (err: unknown) {
      clearInterval(timer)
      setFileError(err instanceof Error ? err.message : "Lỗi khi chuyển đổi giọng nói.")
      setNotice("")
    } finally {
      clearInterval(timer)
      setIsConverting(false)
    }
  }

  const badges = result
    ? [
        `Giọng đích: ${result.voiceName}`,
        `Khoảng cách: ${settings.distance}`,
        `Không gian: ${settings.space}`,
      ]
    : []

  return (
    <section className="motion-screen min-h-full px-4 py-5 sm:px-6 sm:py-6" aria-label="Đổi giọng">
      <div className="mx-auto flex w-full max-w-[840px] flex-col gap-4">
        <header>
          <h2 className="text-[22px] font-semibold tracking-[-0.04em] text-foreground sm:text-[24px]">
            Đổi giọng
          </h2>
          <p className="mt-1 text-[12px] leading-5 text-muted-foreground">
            Tải tệp âm thanh hoặc video lên, chọn giọng đích và xuất âm thanh chất lượng cao 24 kHz trên GPU.
          </p>
        </header>

        {/* TARGET VOICE SELECTOR BAR */}
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-border bg-card p-3 shadow-xs sm:px-4 sm:py-3">
          <div className="flex min-w-0 flex-1 items-center gap-3">
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
                    Giọng đích · {currentVoice.gender} · {currentVoice.style}
                  </p>
                </div>
                <ChevronDown className="ml-1 size-4 text-muted-foreground" />
              </button>

              {/* Dropdown Menu */}
              {voiceDropdownOpen ? (
                <div className="absolute left-0 top-full z-50 mt-1 max-h-[320px] w-[280px] overflow-y-auto rounded-xl border border-border bg-card p-1.5 shadow-xl sm:w-[320px]">
                  <div className="px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    Giọng Tiếng Việt
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

            {/* Quick Chips */}
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

          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => togglePreview(currentVoice)}
              className="h-8 gap-1.5 rounded-lg border-border px-2.5 text-[11px] font-medium"
            >
              <Volume2 className={cn("size-3.5", playingPreview ? "animate-pulse text-primary" : "")} />
              <span>{playingPreview ? "Dừng thử" : "Nghe thử giọng đích"}</span>
            </Button>
          </div>
        </div>

        {/* UPLOAD & SETTINGS CARD */}
        <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
          <div>
            <label
              htmlFor="voice-changer-file"
              onDragOver={(event) => {
                event.preventDefault()
                setIsDragging(true)
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              className={`relative flex min-h-[140px] cursor-pointer flex-col items-center justify-center overflow-hidden rounded-xl border border-dashed px-5 py-6 text-center transition-colors ${
                isDragging
                  ? "border-primary bg-primary/10"
                  : "border-border bg-muted/20 hover:border-primary/40 hover:bg-muted/40"
              }`}
            >
              <input
                ref={inputRef}
                id="voice-changer-file"
                type="file"
                accept="audio/*,video/*,.mp3,.wav,.m4a,.aac,.ogg,.mp4,.mov,.webm"
                className="sr-only"
                onChange={(event) => acceptFile(event.target.files?.[0])}
              />
              <span className="mb-2.5 flex size-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                {selectedFile ? <AudioLines className="size-4" aria-hidden="true" /> : <Upload className="size-4" aria-hidden="true" />}
              </span>
              <span className="max-w-full truncate text-[12px] font-semibold text-foreground">
                {selectedFile ? selectedFile.name : "Thả tệp âm thanh hoặc video vào đây"}
              </span>
              <span className="mt-1 text-[11px] text-muted-foreground">
                {selectedFile
                  ? `${formatFileSize(selectedFile.size)} · Nhấn để chọn tệp khác`
                  : "hoặc nhấn để tải lên · MP3, WAV, M4A, MP4 (tối đa 50 MB)"}
              </span>
            </label>
            {fileError ? <p role="alert" className="mt-2 text-[11px] text-destructive">{fileError}</p> : null}
          </div>

          <label className="mt-4 flex flex-col gap-1.5">
            <div className="flex items-center justify-between">
              <span className="text-[12px] font-semibold text-foreground">
                Văn bản / Câu thoại chuyển đổi
              </span>
              <span className="text-[10px] text-muted-foreground">
                Khuyến nghị nhập câu thoại để giọng đích đọc chuẩn xác nhất
              </span>
            </div>
            <textarea
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              rows={2}
              placeholder="Nhập nội dung thoại trong tệp âm thanh của bạn (để trống sẽ dùng câu chào mặc định của giọng đích)..."
              className="min-h-[72px] w-full resize-y rounded-xl border border-border bg-background px-3 py-2.5 text-[12px] leading-5 text-foreground outline-none placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
          </label>

          {notice ? (
            <p role="status" className="mt-3 rounded-xl border border-primary/20 bg-primary/5 px-3.5 py-2.5 text-[11px] leading-5 text-primary">
              {notice}
            </p>
          ) : null}

          <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-border pt-3">
            <p className="min-w-0 truncate text-[11px] text-muted-foreground">
              {selectedFile ? `${selectedFile.name} · ${formatFileSize(selectedFile.size)}` : "Chưa có tệp được chọn · Tối đa 50 MB"}
            </p>
            <div className="ml-auto flex shrink-0 items-center gap-2">
              {selectedFile ? (
                <Button
                  type="button"
                  variant="ghost"
                  size="icon-sm"
                  aria-label="Xóa tệp đã chọn"
                  onClick={() => {
                    setSelectedFile(null)
                    setFileError("")
                    setNotice("")
                  }}
                  className="size-9 rounded-lg text-muted-foreground hover:bg-muted"
                >
                  <X className="size-4" />
                </Button>
              ) : null}
              <Button
                type="button"
                onClick={handleConvert}
                disabled={!selectedFile || isConverting}
                className="h-9 rounded-lg bg-primary px-4 text-[12px] font-semibold text-primary-foreground hover:bg-primary/90"
              >
                {isConverting ? (
                  <Loader2 className="size-3.5 animate-spin" data-icon="inline-start" />
                ) : (
                  <Sparkles data-icon="inline-start" />
                )}
                {isConverting ? "Đang xử lý trên GPU..." : `Đổi sang giọng ${currentVoice.name}`}
              </Button>
            </div>
          </div>
        </div>

        <StudioWaveformPlayer
          title="Bản ghi sau chuyển đổi (24 kHz WAV)"
          audioUrl={result?.audioUrl}
          filename={result?.filename}
          duration={result?.duration}
          elapsed={result?.elapsed}
          waveform={result?.waveform}
          logs={result?.logs}
          badges={badges}
          emptyTitle="Chưa có bản ghi nào"
          emptyDescription="Tải tệp lên, chọn giọng đích và nhấn “Đổi giọng” để tổng hợp âm thanh bằng giọng đích đã chọn."
        />
      </div>
    </section>
  )
}
