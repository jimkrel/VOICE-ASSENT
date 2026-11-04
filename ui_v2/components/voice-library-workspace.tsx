"use client"

import { useMemo, useRef, useState } from "react"
import Link from "next/link"
import {
  AudioLines,
  Check,
  ChevronDown,
  Mic,
  Pause,
  Play,
  Plus,
  Search,
  Sparkles,
  Trash2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { StudioWaveformPlayer } from "@/components/studio-waveform-player"
import { getVoiceById, voiceCatalog, type VoiceProfile } from "@/lib/voice-catalog"
import { cn } from "@/lib/utils"

type VoiceLibraryWorkspaceProps = {
  selectedVoiceId: string
  onSelectVoice: (voiceId: string) => void
  onUseVoice: (voiceId: string) => void
  onCreateNewVoice?: () => void
  onVoiceDeleted?: (voiceId: string) => void
  voices?: VoiceProfile[]
}

const filters = [
  { id: "all", label: "Tất cả" },
  { id: "Tiếng Việt", label: "Tiếng Việt" },
  { id: "US English", label: "US English" },
  { id: "UK English", label: "UK English" },
  { id: "Nam (Male)", label: "Nam" },
  { id: "Nữ (Female)", label: "Nữ" },
  { id: "Giọng tự tạo", label: "Giọng tự tạo" },
]

const orbStyles: Record<VoiceProfile["tone"], string> = {
  aqua: "bg-[radial-gradient(circle_at_30%_25%,#e3ffff_0%,#64d8ec_28%,#3b83ee_62%,#8755dc_100%)]",
  violet: "bg-[radial-gradient(circle_at_30%_25%,#f3dcff_0%,#b772e2_30%,#5147cc_68%,#312a63_100%)]",
  coral: "bg-[radial-gradient(circle_at_30%_25%,#fff1df_0%,#ff9c70_30%,#df5d74_64%,#684cb9_100%)]",
  blue: "bg-[radial-gradient(circle_at_30%_25%,#d8f7ff_0%,#52c0e9_32%,#2575c8_68%,#183b78_100%)]",
  green: "bg-[radial-gradient(circle_at_30%_25%,#e7fff2_0%,#76d9b0_30%,#398db5_66%,#566fda_100%)]",
}

function VoiceOrb({ voice, size = "size-10" }: { voice: VoiceProfile; size?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "block shrink-0 rounded-full border border-white/70 shadow-[0_2px_7px_rgba(35,69,120,0.16)]",
        size,
        orbStyles[voice.tone] || orbStyles.aqua
      )}
    />
  )
}

function VoiceRow({
  voice,
  selected,
  playing,
  onSelect,
  onPreview,
  onUse,
  onDelete,
}: {
  voice: VoiceProfile
  selected: boolean
  playing: boolean
  onSelect: () => void
  onPreview: () => void
  onUse: () => void
  onDelete?: () => void
}) {
  const isCustom = voice.id.startsWith("custom-") || voice.source === "Giọng tự tạo"

  return (
    <article
      className={cn(
        "group flex flex-col gap-3 rounded-xl border p-3 transition-all sm:flex-row sm:items-center",
        selected
          ? "border-primary/50 bg-primary/5 shadow-2xs"
          : "border-border bg-card hover:border-primary/30 hover:bg-muted/30"
      )}
    >
      <div className="flex min-w-0 flex-1 items-center gap-3">
        {/* Prominent Instant Play/Pause Button (ElevenLabs / Spotify preview style) */}
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            onPreview()
          }}
          aria-label={playing ? `Dừng nghe mẫu ${voice.name}` : `Nghe thử mẫu ${voice.name}`}
          title={playing ? "Dừng phát mẫu" : "Bấm để nghe thử ngay đoạn voice mẫu"}
          className={cn(
            "relative flex size-11 shrink-0 items-center justify-center rounded-full transition-all duration-200 shadow-sm",
            playing
              ? "bg-primary text-primary-foreground scale-105 shadow-primary/30 shadow-md ring-4 ring-primary/20"
              : "bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground hover:scale-105 active:scale-95"
          )}
        >
          {playing ? (
            <div className="flex items-center gap-0.5">
              <span className="h-3.5 w-1 rounded-full bg-current animate-bounce [animation-delay:-0.3s]" />
              <span className="h-4.5 w-1 rounded-full bg-current animate-bounce [animation-delay:-0.15s]" />
              <span className="h-3 w-1 rounded-full bg-current animate-bounce" />
            </div>
          ) : (
            <Play className="ml-0.5 size-4 fill-current" />
          )}
        </button>

        <VoiceOrb voice={voice} size="size-9" />

        <button
          type="button"
          onClick={onSelect}
          aria-pressed={selected}
          className="min-w-0 flex-1 text-left focus:outline-none"
        >
          <div className="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-0.5">
            <span className="truncate text-[12px] font-semibold text-foreground">
              {voice.name} — {voice.style}
            </span>
            <span className="rounded-full bg-muted px-2 py-0.5 text-[10px] text-muted-foreground">
              {voice.source}
            </span>
            {playing ? (
              <span className="flex items-center gap-1 rounded-full bg-primary/15 px-2 py-0.5 text-[10px] font-medium text-primary">
                <span className="size-1.5 rounded-full bg-primary animate-ping" />
                Đang phát mẫu...
              </span>
            ) : null}
          </div>
          <span className="mt-0.5 block truncate text-[11px] text-muted-foreground">
            {voice.language} · {voice.gender} · {voice.description}
          </span>
          <span className="mt-0.5 block truncate text-[11px] italic text-muted-foreground/85">
            “{voice.sampleText}”
          </span>
        </button>
      </div>

      <div className="flex shrink-0 items-center gap-2 pl-[56px] sm:pl-0">
        {isCustom && onDelete && voice.id.startsWith("custom-") ? (
          <Button
            type="button"
            variant="ghost"
            size="icon-sm"
            aria-label={`Xóa giọng ${voice.name}`}
            onClick={onDelete}
            className="size-8 rounded-lg text-destructive hover:bg-destructive/10"
          >
            <Trash2 className="size-3.5" />
          </Button>
        ) : null}
        <Button
          type="button"
          variant={selected ? "secondary" : "outline"}
          size="sm"
          onClick={onUse}
          className="h-8 rounded-lg border-border px-3 text-[11px] font-medium"
        >
          {selected ? <Check data-icon="inline-start" /> : <Mic data-icon="inline-start" />}
          Dùng giọng này
        </Button>
      </div>
    </article>
  )
}

export function VoiceLibraryWorkspace({
  selectedVoiceId,
  onSelectVoice,
  onUseVoice,
  onCreateNewVoice,
  onVoiceDeleted,
  voices = voiceCatalog,
}: VoiceLibraryWorkspaceProps) {
  const [activeFilter, setActiveFilter] = useState("all")
  const [searchValue, setSearchValue] = useState("")
  const [notice, setNotice] = useState("")
  const [playingId, setPlayingId] = useState<string | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const selectedVoice = getVoiceById(selectedVoiceId, voices)

  const filteredVoices = useMemo(() => {
    const query = searchValue.trim().toLocaleLowerCase("vi")
    return voices.filter((voice) => {
      const matchesFilter =
        activeFilter === "all" ||
        voice.categories.includes(activeFilter) ||
        (activeFilter === "Giọng tự tạo" && voice.source === "Giọng tự tạo")
      const searchableText = `${voice.name} ${voice.style} ${voice.description} ${voice.language}`.toLocaleLowerCase("vi")
      return matchesFilter && (!query || searchableText.includes(query))
    })
  }, [activeFilter, searchValue, voices])

  function handlePreview(voice: VoiceProfile) {
    if (playingId === voice.id && audioRef.current) {
      audioRef.current.pause()
      setPlayingId(null)
      setNotice("")
      return
    }
    if (audioRef.current) {
      audioRef.current.pause()
    }
    const url = voice.previewUrl || `/api/voices/${voice.id}/preview`
    const audio = new Audio(url)
    audioRef.current = audio
    setPlayingId(voice.id)
    setNotice(`Đang phát mẫu giọng “${voice.name}” — “${voice.sampleText}”`)
    audio.onended = () => {
      setPlayingId(null)
      setNotice("")
    }
    audio.onerror = () => {
      setPlayingId(null)
      setNotice(`Không thể phát tệp mẫu của giọng “${voice.name}”.`)
    }
    audio.play().catch(() => {
      setPlayingId(null)
    })
  }

  async function handleDeleteVoice(voice: VoiceProfile) {
    try {
      const res = await fetch(`/api/voices/${voice.id}`, { method: "DELETE" })
      const data = await res.json()
      if (!res.ok) {
        setNotice(data.detail || "Không thể xóa giọng đọc này.")
        return
      }
      setNotice(data.message || `Đã xóa giọng “${voice.name}”.`)
      onVoiceDeleted?.(voice.id)
    } catch {
      setNotice("Lỗi kết nối khi xóa giọng đọc.")
    }
  }

  function handleUseVoice() {
    if (audioRef.current) {
      audioRef.current.pause()
      setPlayingId(null)
    }
    setNotice("")
    onUseVoice(selectedVoice.id)
  }

  const selectedPreviewUrl = selectedVoice.previewUrl || `/api/voices/${selectedVoice.id}/preview`

  return (
    <section className="motion-screen min-h-full px-4 py-5 sm:px-6 sm:py-6" aria-label="Kho giọng đọc">
      <div className="mx-auto flex w-full max-w-[940px] flex-col gap-4">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-[22px] font-semibold tracking-[-0.04em] text-foreground sm:text-[24px]">
              Kho giọng đọc
            </h2>
            <p className="mt-1 text-[12px] leading-5 text-muted-foreground">
              Khám phá {voices.length} giọng đọc mẫu phòng thu (Tiếng Việt &amp; Quốc tế) hoặc quản lý giọng tự tạo.
            </p>
          </div>
          <Link
            href="/voice-creation"
            onClick={onCreateNewVoice}
            className="inline-flex h-9 items-center gap-1.5 rounded-xl border border-border bg-card px-3.5 text-[11px] font-semibold text-foreground shadow-xs transition-colors hover:bg-muted"
          >
            <Plus className="size-3.5" aria-hidden="true" />
            Tạo giọng mới
          </Link>
        </header>

        <section className="rounded-2xl border border-border bg-card p-3.5 shadow-sm sm:p-4" aria-label="Giọng đọc đang chọn">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <label className="relative min-w-0 flex-1">
              <span className="sr-only">Chọn giọng đọc</span>
              <select
                value={selectedVoice.id}
                onChange={(event) => {
                  onSelectVoice(event.target.value)
                  setNotice("")
                }}
                className="h-10 w-full appearance-none rounded-xl border border-border bg-background pl-3 pr-9 text-[11px] text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                {voices.map((voice) => (
                  <option key={voice.id} value={voice.id}>{`${voice.name} — ${voice.style}`}</option>
                ))}
              </select>
              <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
            </label>
            <Button
              type="button"
              onClick={handleUseVoice}
              className="h-10 rounded-xl bg-primary px-4 text-[11px] font-semibold text-primary-foreground hover:bg-primary/90"
            >
              <Mic data-icon="inline-start" />
              Dùng giọng này cho kịch bản
            </Button>
          </div>

          <div className="mt-3">
            <StudioWaveformPlayer
              title={`Mẫu giọng Studio: ${selectedVoice.name} (${selectedVoice.language} · ${selectedVoice.gender})`}
              subtitle={`“${selectedVoice.sampleText}”`}
              audioUrl={selectedPreviewUrl}
              filename={`${selectedVoice.id}_sample.wav`}
              duration={6.5}
              elapsed={0.1}
              badges={[selectedVoice.source, selectedVoice.language, selectedVoice.description]}
            />
          </div>
          {notice ? <p role="status" className="mt-2 rounded-lg bg-primary/10 px-3 py-2 text-[11px] leading-5 text-primary">{notice}</p> : null}
        </section>

        <div className="mt-1 flex flex-col gap-3">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h3 className="text-[13px] font-semibold text-foreground">Tất cả giọng đọc</h3>
              <p className="mt-0.5 text-[11px] text-muted-foreground">{filteredVoices.length} giọng phù hợp</p>
            </div>
            <label className="flex h-9 w-full items-center gap-2 rounded-xl border border-border bg-background px-3 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 sm:max-w-[300px]">
              <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
              <input
                type="search"
                value={searchValue}
                onChange={(event) => setSearchValue(event.target.value)}
                placeholder="Tìm giọng đọc..."
                aria-label="Tìm kiếm giọng đọc"
                className="min-w-0 flex-1 bg-transparent text-[11px] text-foreground outline-none placeholder:text-muted-foreground"
              />
            </label>
          </div>

          <div className="flex gap-1.5 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden" role="group" aria-label="Lọc giọng đọc">
            {filters.map((filter) => {
              const isActive = activeFilter === filter.id
              return (
                <button
                  key={filter.id}
                  type="button"
                  aria-pressed={isActive}
                  onClick={() => setActiveFilter(filter.id)}
                  className={cn(
                    "inline-flex h-8 shrink-0 items-center rounded-lg border px-3 text-[11px] font-medium transition-colors",
                    isActive
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground"
                  )}
                >
                  {filter.label}
                </button>
              )
            })}
          </div>
        </div>

        <div className="flex flex-col gap-2">
          {filteredVoices.length > 0 ? filteredVoices.map((voice) => (
            <VoiceRow
              key={voice.id}
              voice={voice}
              selected={selectedVoice.id === voice.id}
              playing={playingId === voice.id}
              onSelect={() => {
                onSelectVoice(voice.id)
                setNotice("")
              }}
              onPreview={() => handlePreview(voice)}
              onUse={() => onUseVoice(voice.id)}
              onDelete={() => handleDeleteVoice(voice)}
            />
          )) : (
            <div className="rounded-2xl border border-dashed border-border bg-card px-5 py-10 text-center">
              <Sparkles className="mx-auto size-5 text-muted-foreground" aria-hidden="true" />
              <p className="mt-2 text-[12px] font-medium text-foreground">Không tìm thấy giọng phù hợp</p>
              <p className="mt-1 text-[11px] text-muted-foreground">Thử từ khóa khác hoặc chọn danh mục khác.</p>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
