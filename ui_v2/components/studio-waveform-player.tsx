"use client"

import { useEffect, useRef, useState } from "react"
import {
  Activity,
  AudioLines,
  CheckCircle2,
  Download,
  Pause,
  Play,
  Terminal,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export type StudioLogItem = {
  time: string
  message: string
}

export function StudioWaveformPlayer({
  title,
  subtitle,
  audioUrl,
  filename,
  duration,
  elapsed,
  waveform = [],
  logs = [],
  badges = [],
  emptyTitle = "Chưa có bản ghi nào",
  emptyDescription = "Kết quả sóng âm, trình phát và nhật ký xử lý sẽ hiển thị tại đây.",
}: {
  title: string
  subtitle?: string
  audioUrl?: string | null
  filename?: string | null
  duration?: number
  elapsed?: number
  waveform?: number[]
  logs?: StudioLogItem[]
  badges?: string[]
  emptyTitle?: string
  emptyDescription?: string
}) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [playPct, setPlayPct] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const [decodedBars, setDecodedBars] = useState<number[]>([])
  const [decodedDuration, setDecodedDuration] = useState<number | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    setIsPlaying(false)
    setPlayPct(0)
    setCurrentTime(0)
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
    }
    if (!audioUrl || waveform.length > 0) {
      setDecodedBars([])
      setDecodedDuration(null)
      return
    }
    let cancelled = false
    async function extractClientWaveform(url: string) {
      try {
        const res = await fetch(url)
        if (!res.ok) return
        const buf = await res.arrayBuffer()
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
        const ctx = new AudioCtx()
        const audioBuffer = await ctx.decodeAudioData(buf)
        if (cancelled) {
          ctx.close().catch(() => {})
          return
        }
        const channel = audioBuffer.getChannelData(0)
        const numBars = 64
        const chunkSize = Math.max(1, Math.floor(channel.length / numBars))
        const rmsList: number[] = []
        for (let i = 0; i < numBars; i++) {
          let sum = 0
          const start = i * chunkSize
          const end = Math.min(channel.length, start + chunkSize)
          for (let j = start; j < end; j++) {
            sum += channel[j] * channel[j]
          }
          rmsList.push(Math.sqrt(sum / Math.max(1, end - start)))
        }
        const peak = Math.max(...rmsList, 1e-6)
        const bars64 = rmsList.map((v) =>
          Math.max(14, Math.min(96, Math.round(14 + Math.pow(v / peak, 0.65) * 82)))
        )
        setDecodedBars(bars64)
        setDecodedDuration(Math.round(audioBuffer.duration * 10) / 10)
        ctx.close().catch(() => {})
      } catch {
        // Fallback if Web Audio API cannot decode
      }
    }
    extractClientWaveform(audioUrl)
    return () => {
      cancelled = true
    }
  }, [audioUrl, waveform.length])

  function togglePlay() {
    if (!audioUrl) return
    if (isPlaying && audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
      return
    }
    if (!audioRef.current) {
      const audio = new Audio(audioUrl)
      audioRef.current = audio
      audio.ontimeupdate = () => {
        setCurrentTime(audio.currentTime)
        if (audio.duration > 0) {
          setPlayPct((audio.currentTime / audio.duration) * 100)
        }
      }
      audio.onended = () => {
        setIsPlaying(false)
        setPlayPct(100)
      }
      audio.onerror = () => {
        setIsPlaying(false)
      }
    }
    setIsPlaying(true)
    audioRef.current.play().catch(() => setIsPlaying(false))
  }

  const effectiveDuration = duration ?? decodedDuration ?? 6.5
  const bars =
    waveform.length > 0
      ? waveform
      : decodedBars.length > 0
        ? decodedBars
        : Array.from({ length: 64 }, (_, i) =>
            Math.max(18, Math.min(90, Math.round(24 + Math.sin(i * 0.45) * 28 + Math.cos(i * 0.9) * 22)))
          )
  const activeBars = audioUrl ? Math.round(((playPct > 0 ? playPct : 100) / 100) * bars.length) : 0

  return (
    <section
      className="rounded-2xl border border-border/80 bg-card p-3.5 shadow-sm sm:p-4"
      aria-label={title}
    >
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex min-w-0 items-center gap-2.5">
          <span
            className={cn(
              "flex size-8 shrink-0 items-center justify-center rounded-xl border",
              audioUrl
                ? "border-primary/35 bg-primary/10 text-primary"
                : "border-border bg-muted/50 text-muted-foreground"
            )}
          >
            <AudioLines className="size-4" aria-hidden="true" />
          </span>
          <div className="min-w-0">
            <h3 className="truncate text-[12px] font-semibold text-foreground">{title}</h3>
            <p className="mt-0.5 truncate text-[11px] text-muted-foreground">
              {subtitle ||
                (audioUrl
                  ? `${filename || "studio_out.wav"} · ${duration ?? 0}s âm thanh (xử lý ${elapsed ?? 0}s) · 24 kHz WAV`
                  : "Chờ xử lý trên GPU")}
            </p>
          </div>
        </div>

        {audioUrl ? (
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={togglePlay}
              className="h-8 rounded-lg px-2.5 text-[11px] font-medium"
            >
              {isPlaying ? (
                <Pause className="size-3.5 fill-current" data-icon="inline-start" />
              ) : (
                <Play className="size-3.5 fill-current" data-icon="inline-start" />
              )}
              {isPlaying ? "Tạm dừng" : "Phát sóng âm"}
            </Button>
            <a
              href={audioUrl}
              download={filename || "voice_output.wav"}
              className="inline-flex h-8 items-center gap-1.5 rounded-lg border border-border bg-muted/40 px-3 text-[11px] font-medium text-foreground hover:bg-muted"
            >
              <Download className="size-3.5 text-primary" />
              Tải WAV
            </a>
          </div>
        ) : null}
      </div>

      {audioUrl ? (
        <div className="flex flex-col gap-3 rounded-xl border border-border/70 bg-muted/20 p-3 sm:p-3.5">
          {/* Interactive 64-bar Studio Waveform */}
          <div
            role="img"
            aria-label="Biểu đồ sóng âm thực tế"
            data-playing={isPlaying}
            onClick={togglePlay}
            className="relative flex h-[84px] w-full cursor-pointer items-center justify-between gap-[2px] overflow-hidden rounded-lg border border-border/70 bg-background/90 px-3 py-2.5 shadow-inner sm:gap-1"
          >
            {bars.map((h, idx) => {
              const filled = idx < activeBars
              return (
                <span
                  key={idx}
                  className={cn(
                    "waveform-bar min-h-1.5 flex-1 rounded-full transition-all duration-150",
                    filled
                      ? "bg-linear-to-t from-primary/80 via-primary to-primary"
                      : "bg-muted-foreground/20"
                  )}
                  style={{
                    height: `${h}%`,
                    animationDelay: `${(idx % 14) * 40}ms`,
                  }}
                />
              )
            })}
            <span
              aria-hidden="true"
              className="pointer-events-none absolute inset-y-1 w-0.5 bg-primary shadow-[0_0_8px_var(--primary)] transition-[left] duration-100 ease-linear"
              style={{ left: `${Math.min(99, Math.max(1, playPct > 0 ? playPct : 100))}%` }}
            />
          </div>

          <div className="flex items-center justify-between text-[10px] font-mono text-muted-foreground">
            <span>{currentTime.toFixed(1)}s</span>
            <span>24 kHz · -14 LUFS Studio Master</span>
            <span>{effectiveDuration.toFixed(1)}s</span>
          </div>

          <audio key={audioUrl} controls src={audioUrl} className="h-9 w-full" />

          {badges.length > 0 ? (
            <div className="flex flex-wrap items-center gap-1.5 text-[10px] text-muted-foreground">
              {badges.map((b, i) => (
                <span
                  key={i}
                  className={cn(
                    "rounded-md border px-2 py-0.5",
                    i === 0
                      ? "border-primary/25 bg-primary/10 font-medium text-primary"
                      : "border-border bg-background"
                  )}
                >
                  {b}
                </span>
              ))}
            </div>
          ) : null}

          {logs.length > 0 ? (
            <div className="rounded-lg border border-border/60 bg-background/80 p-2.5">
              <div className="mb-1.5 flex items-center justify-between text-[10px] font-semibold text-foreground">
                <span className="flex items-center gap-1.5">
                  <Terminal className="size-3 text-muted-foreground" />
                  Nhật ký xử lý GPU ({logs.length} bước)
                </span>
                <span className="font-mono text-[9px] text-chart-3">● Đã hoàn tất</span>
              </div>
              <ol className="flex max-h-[110px] flex-col gap-1 overflow-y-auto text-[10px]">
                {logs.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="mt-0.5 size-3 shrink-0 text-primary" />
                    <time className="shrink-0 font-mono text-[9px] text-muted-foreground">
                      {item.time}
                    </time>
                    <span className="text-foreground/90">{item.message}</span>
                  </li>
                ))}
              </ol>
            </div>
          ) : null}
        </div>
      ) : (
        <div className="flex min-h-[76px] items-center gap-3 rounded-xl border border-dashed border-border/80 bg-muted/20 px-3.5 py-3 sm:px-4">
          <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <Activity className="size-4" aria-hidden="true" />
          </span>
          <div className="min-w-0">
            <p className="text-[12px] font-medium text-foreground">{emptyTitle}</p>
            <p className="mt-0.5 text-[11px] leading-4 text-muted-foreground">
              {emptyDescription}
            </p>
          </div>
        </div>
      )}
    </section>
  )
}
