"use client"

import { useRef, useState, type DragEvent, type FormEvent } from "react"
import { AudioLines, Check, Loader2, Mic, Sparkles, Upload } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { StudioWaveformPlayer, type StudioLogItem } from "@/components/studio-waveform-player"
import { VoiceGenerationDemo } from "@/components/voice-generation-demo"
import type { VoiceProfile } from "@/lib/voice-catalog"

type UploadedAudio = {
  name: string
  size: number
  file: File
}

const MAX_AUDIO_SIZE = 50 * 1024 * 1024

function formatFileSize(size: number) {
  return size < 1024 * 1024
    ? `${Math.max(1, Math.round(size / 1024))} KB`
    : `${(size / (1024 * 1024)).toFixed(1)} MB`
}

function AudioUploadField({
  audio,
  error,
  onAudioSelect,
}: {
  audio: UploadedAudio | null
  error: string
  onAudioSelect: (file?: File) => void
}) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault()
    setIsDragging(false)
    onAudioSelect(event.dataTransfer.files[0])
  }

  return (
    <div>
      <label
        htmlFor="voice-clone-audio"
        onDragOver={(event) => {
          event.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`relative flex min-h-[132px] cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed px-4 py-4 text-center transition-colors ${
          isDragging
            ? "border-primary bg-primary/10"
            : "border-border bg-muted/20 hover:border-primary/40 hover:bg-muted/40"
        }`}
      >
        <input
          ref={inputRef}
          id="voice-clone-audio"
          type="file"
          accept="audio/*,.mp3,.wav,.m4a,.ogg"
          className="sr-only"
          onChange={(event) => onAudioSelect(event.target.files?.[0])}
        />
        <span className="mb-2.5 flex size-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
          {audio ? <AudioLines className="size-4" aria-hidden="true" /> : <Upload className="size-4" aria-hidden="true" />}
        </span>
        <span className="max-w-full truncate text-[12px] font-semibold text-foreground">
          {audio ? audio.name : "Thả tệp âm thanh vào đây"}
        </span>
        <span className="mt-1 text-[11px] text-muted-foreground">
          {audio
            ? `${formatFileSize(audio.size)} · Nhấn để chọn tệp khác`
            : "hoặc nhấn để tải lên · MP3, WAV, M4A"}
        </span>
        {!audio ? <span className="mt-2 text-[10px] text-muted-foreground">Mẫu giọng khuyến nghị: 5–15 giây</span> : null}
      </label>
      <div className="mt-2 flex items-start justify-between gap-3 text-[10px] leading-4 text-muted-foreground">
        <span>Chọn đoạn ghi âm rõ, không có nhạc nền hoặc tiếng ồn.</span>
        <span className="shrink-0">Tối đa 50 MB</span>
      </div>
      {error ? <p role="alert" className="mt-2 text-[11px] text-destructive">{error}</p> : null}
    </div>
  )
}

function VoiceNameField({
  value,
  onChange,
}: {
  value: string
  onChange: (value: string) => void
}) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-[12px] font-semibold text-foreground">Tên giọng đọc mới</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        maxLength={60}
        placeholder="Ví dụ: Giọng MC Minh Quân"
        className="h-10 w-full rounded-xl border border-border bg-background px-3 text-[12px] text-foreground outline-none placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20"
      />
    </label>
  )
}

export function VoiceCreationWorkspace({
  selectedVoiceId = "minh-anh",
  onVoiceCreated,
  onUseVoice,
  onGenerated,
}: {
  selectedVoiceId?: string
  onVoiceCreated?: (voice: VoiceProfile) => void
  onUseVoice?: (voiceId: string) => void
  onGenerated?: () => void
}) {
  const [name, setName] = useState("")
  const [audio, setAudio] = useState<UploadedAudio | null>(null)
  const [transcript, setTranscript] = useState("")
  const [designPrompt, setDesignPrompt] = useState("")
  const [designLang, setDesignLang] = useState("Tiếng Việt")
  const [designStyle, setDesignStyle] = useState("Tự nhiên")
  const [audioError, setAudioError] = useState("")
  const [formError, setFormError] = useState("")
  const [notice, setNotice] = useState("")
  const [createdVoice, setCreatedVoice] = useState<{
    id: string
    name: string
    audioUrl: string
    waveform?: number[]
    logs?: StudioLogItem[]
    modeLabel: string
  } | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  function acceptAudio(file?: File) {
    if (!file) return

    const isAudio = file.type.startsWith("audio/") || /\.(mp3|wav|m4a|ogg|aac|flac)$/i.test(file.name)
    if (!isAudio) {
      setAudio(null)
      setAudioError("Vui lòng chọn tệp âm thanh MP3, WAV, M4A hoặc OGG.")
      return
    }
    if (file.size > MAX_AUDIO_SIZE) {
      setAudio(null)
      setAudioError("Tệp âm thanh cần có dung lượng dưới 50 MB.")
      return
    }

    setAudio({ name: file.name, size: file.size, file })
    setAudioError("")
    setFormError("")
    setNotice("")
  }

  async function handleCloneSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!name.trim() || !audio || !transcript.trim()) {
      setFormError("Vui lòng điền tên giọng, tải mẫu âm thanh và nhập chính xác câu thoại trong bản ghi.")
      return
    }
    setIsSubmitting(true)
    setFormError("")
    setNotice("Đang xử lý mẫu âm thanh và trích xuất đặc trưng trên GPU...")
    const startCloneTime = Date.now()
    const cloneTimer = setInterval(() => {
      const elapsedSec = ((Date.now() - startCloneTime) / 1000).toFixed(1)
      setNotice(`Đang tạo bản sao giọng nói trên GPU (${elapsedSec}s)...`)
    }, 400)
    try {
      const fd = new FormData()
      fd.append("name", name.trim())
      fd.append("transcript", transcript.trim())
      fd.append("audio", audio.file)

      const res = await fetch("/api/voices/clone", {
        method: "POST",
        body: fd,
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || "Không thể sao chép giọng đọc.")
      }
      clearInterval(cloneTimer)
      setNotice(data.message || `Đã tạo giọng “${name}” thành công!`)
      if (data.voice) {
        onVoiceCreated?.(data.voice)
        setCreatedVoice({
          id: data.voice.id,
          name: data.voice.name,
          audioUrl: data.audioUrl || data.voice.sampleUrl,
          waveform: Array.isArray(data.waveform) ? data.waveform : undefined,
          logs: Array.isArray(data.logs) ? data.logs : undefined,
          modeLabel: "Sao chép từ mẫu âm thanh · 24kHz WAV",
        })
      }
      onGenerated?.()
    } catch (err: unknown) {
      clearInterval(cloneTimer)
      setFormError(err instanceof Error ? err.message : "Lỗi khi sao chép giọng đọc.")
      setNotice("")
    } finally {
      clearInterval(cloneTimer)
      setIsSubmitting(false)
    }
  }

  async function handleDesignSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!name.trim() || !designPrompt.trim()) {
      setFormError("Vui lòng điền tên và mô tả giọng đọc bạn muốn thiết kế.")
      return
    }
    setIsSubmitting(true)
    setFormError("")
    setCreatedVoice(null)
    setNotice("Đang khởi tạo mô hình OmniVoice và nạp prompt...")
    const startDesignTime = Date.now()
    const designTimer = setInterval(() => {
      const elapsedSec = ((Date.now() - startDesignTime) / 1000).toFixed(1)
      setNotice(`Đang tổng hợp giọng mới từ mô tả trên GPU (${elapsedSec}s)...`)
    }, 400)
    try {
      const res = await fetch("/api/voices/design", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          prompt: `${designPrompt.trim()} (${designStyle})`,
          language: designLang,
        }),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || "Không thể thiết kế giọng đọc.")
      }
      clearInterval(designTimer)
      setNotice(data.message || `Đã thiết kế giọng “${name}” thành công!`)
      if (data.voice) {
        onVoiceCreated?.(data.voice)
        setCreatedVoice({
          id: data.voice.id,
          name: data.voice.name,
          audioUrl: data.audioUrl || data.voice.sampleUrl,
          waveform: Array.isArray(data.waveform) ? data.waveform : undefined,
          logs: Array.isArray(data.logs) ? data.logs : undefined,
          modeLabel: `Thiết kế giọng AI (${designLang} · ${designStyle}) · 24kHz WAV`,
        })
      }
      onGenerated?.()
    } catch (err: unknown) {
      clearInterval(designTimer)
      setFormError(err instanceof Error ? err.message : "Lỗi khi thiết kế giọng đọc.")
      setNotice("")
    } finally {
      clearInterval(designTimer)
      setIsSubmitting(false)
    }
  }

  return (
    <section className="motion-screen min-h-full px-4 py-5 sm:px-6 sm:py-6" aria-label="Tạo giọng đọc mới">
      <div className="mx-auto w-full max-w-[820px]">
        <header className="mb-4">
          <h2 className="text-[22px] font-semibold tracking-[-0.04em] text-foreground sm:text-[24px]">
            Tạo giọng đọc mới
          </h2>
          <p className="mt-1 text-[12px] leading-5 text-muted-foreground">
            Sao chép từ mẫu âm thanh hoặc thiết kế giọng đọc từ mô tả bằng mô hình AI.
          </p>
        </header>

        <VoiceGenerationDemo selectedVoiceId={selectedVoiceId} onGenerated={onGenerated} />

        <Tabs defaultValue="clone" className="w-full">
          <TabsList
            variant="line"
            className="h-10 w-full justify-start gap-5 rounded-none border-b border-border bg-transparent p-0"
          >
            <TabsTrigger
              value="clone"
              className="h-10 flex-none rounded-none px-1 text-[12px] font-medium text-muted-foreground data-active:text-primary"
            >
              <Mic data-icon="inline-start" />
              Sao chép từ mẫu
            </TabsTrigger>
            <TabsTrigger
              value="design"
              className="h-10 flex-none rounded-none px-1 text-[12px] font-medium text-muted-foreground data-active:text-primary"
            >
              <Sparkles data-icon="inline-start" />
              Thiết kế giọng
            </TabsTrigger>
          </TabsList>

          <TabsContent value="clone" className="pt-4">
            <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
              <p className="mb-4 text-[12px] leading-5 text-muted-foreground">
                Dùng bản ghi ngắn từ 5–15 giây cùng bản chép lời chính xác để tạo giọng mới.
              </p>
              <form onSubmit={handleCloneSubmit} className="flex flex-col gap-4">
                <VoiceNameField value={name} onChange={setName} />
                <div>
                  <p className="mb-2 text-[12px] font-semibold text-foreground">Mẫu âm thanh</p>
                  <AudioUploadField audio={audio} error={audioError} onAudioSelect={acceptAudio} />
                </div>
                <label htmlFor="clone-transcript" className="flex flex-col gap-1.5">
                  <span className="text-[12px] font-semibold text-foreground">Bản chép lời chính xác</span>
                  <textarea
                    id="clone-transcript"
                    value={transcript}
                    onChange={(event) => setTranscript(event.target.value)}
                    rows={3}
                    placeholder="Nhập chính xác câu nói trong đoạn ghi âm..."
                    className="min-h-[76px] w-full resize-y rounded-xl border border-border bg-background px-3 py-2.5 text-[12px] leading-5 text-foreground outline-none placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20"
                  />
                </label>

                {formError ? <p role="alert" className="text-[11px] text-destructive">{formError}</p> : null}
                {notice ? <p role="status" className="rounded-xl border border-primary/20 bg-primary/5 px-3.5 py-2.5 text-[11px] leading-5 text-primary">{notice}</p> : null}

                <Button
                  type="submit"
                  disabled={!name.trim() || !audio || !transcript.trim() || isSubmitting}
                  className="h-10 w-full rounded-xl bg-primary text-[12px] font-semibold text-primary-foreground hover:bg-primary/90 sm:w-auto sm:self-end sm:px-5"
                >
                  {isSubmitting ? <Loader2 className="size-3.5 animate-spin" data-icon="inline-start" /> : <Mic data-icon="inline-start" />}
                  {isSubmitting ? "Đang tạo bản sao..." : "Tạo bản sao giọng nói"}
                </Button>
              </form>
            </div>
          </TabsContent>

          <TabsContent value="design" className="pt-4">
            <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
              <p className="mb-4 text-[12px] leading-5 text-muted-foreground">
                Mô tả chất giọng, ngữ điệu và tính cách để tạo một giọng đọc mới.
              </p>
              <form onSubmit={handleDesignSubmit} className="flex flex-col gap-4">
                <VoiceNameField value={name} onChange={setName} />
                <label htmlFor="voice-design-prompt" className="flex flex-col gap-1.5">
                  <span className="text-[12px] font-semibold text-foreground">Mô tả giọng đọc</span>
                  <textarea
                    id="voice-design-prompt"
                    value={designPrompt}
                    onChange={(event) => setDesignPrompt(event.target.value)}
                    rows={5}
                    maxLength={1000}
                    placeholder="Ví dụ: Giọng nữ miền Bắc, trưởng thành, ấm áp, phát âm rõ và nhịp kể chậm..."
                    className="min-h-[150px] w-full resize-y rounded-xl border border-border bg-background px-3 py-2.5 text-[12px] leading-5 text-foreground outline-none placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20"
                  />
                  <span className="flex items-center justify-between gap-3 text-[10px] text-muted-foreground">
                    <span>Mô tả giọng, vùng miền và cảm xúc</span>
                    <span className="tabular-nums">{designPrompt.length} / 1.000</span>
                  </span>
                </label>
                <div className="grid gap-3 sm:grid-cols-2">
                  <label className="flex flex-col gap-1.5">
                    <span className="text-[12px] font-semibold text-foreground">Ngôn ngữ</span>
                    <select
                      value={designLang}
                      onChange={(e) => setDesignLang(e.target.value)}
                      className="h-10 rounded-xl border border-border bg-card px-3 text-[12px] text-foreground outline-none focus:border-primary"
                    >
                      <option>Tiếng Việt</option>
                      <option>English</option>
                      <option>Đa ngôn ngữ</option>
                    </select>
                  </label>
                  <label className="flex flex-col gap-1.5">
                    <span className="text-[12px] font-semibold text-foreground">Phong cách</span>
                    <select
                      value={designStyle}
                      onChange={(e) => setDesignStyle(e.target.value)}
                      className="h-10 rounded-xl border border-border bg-card px-3 text-[12px] text-foreground outline-none focus:border-primary"
                    >
                      <option>Tự nhiên</option>
                      <option>Phát thanh</option>
                      <option>Kể chuyện</option>
                      <option>Quảng cáo</option>
                    </select>
                  </label>
                </div>

                {formError ? <p role="alert" className="text-[11px] text-destructive">{formError}</p> : null}
                {notice ? <p role="status" className="rounded-xl border border-primary/20 bg-primary/5 px-3.5 py-2.5 text-[11px] leading-5 text-primary">{notice}</p> : null}
                <Button
                  type="submit"
                  disabled={!name.trim() || !designPrompt.trim() || isSubmitting}
                  className="h-10 w-full rounded-xl bg-primary text-[12px] font-semibold text-primary-foreground hover:bg-primary/90 sm:w-auto sm:self-end sm:px-5"
                >
                  {isSubmitting ? <Loader2 className="size-3.5 animate-spin" data-icon="inline-start" /> : <Check data-icon="inline-start" />}
                  {isSubmitting ? "Đang thiết kế..." : "Thiết kế giọng đọc"}
                </Button>
              </form>
            </div>
          </TabsContent>
        </Tabs>

        {createdVoice ? (
          <div className="mt-4">
            <StudioWaveformPlayer
              audioUrl={createdVoice.audioUrl}
              title={`Giọng mới đã lưu: ${createdVoice.name}`}
              subtitle={createdVoice.modeLabel}
              filename={`${createdVoice.id}.wav`}
              waveform={createdVoice.waveform}
              logs={createdVoice.logs}
              badges={["Đã thêm vào Kho giọng đọc"]}
            />
            {onUseVoice ? (
              <div className="mt-2.5 flex justify-end">
                <Button
                  type="button"
                  onClick={() => onUseVoice(createdVoice.id)}
                  className="h-9 rounded-xl bg-primary px-4 text-[12px] font-semibold text-primary-foreground hover:bg-primary/90"
                >
                  Dùng giọng “{createdVoice.name}” đọc kịch bản ngay
                </Button>
              </div>
            ) : null}
          </div>
        ) : null}

        <p className="mt-4 flex items-center gap-2 text-[10px] leading-4 text-muted-foreground">
          <AudioLines className="size-3.5 shrink-0" aria-hidden="true" />
          Giọng mới sau khi tạo sẽ được lưu trực tiếp vào Kho giọng đọc của bạn.
        </p>
      </div>
    </section>
  )
}
