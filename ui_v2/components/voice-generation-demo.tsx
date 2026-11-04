"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import {
  Activity,
  AudioLines,
  Check,
  Cpu,
  HardDrive,
  LoaderCircle,
  Play,
  RotateCcw,
  Sparkles,
  Terminal,
  type LucideIcon,
} from "lucide-react"
import {
  CartesianGrid,
  Line,
  LineChart,
  XAxis,
  YAxis,
} from "recharts"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart"
import { cn } from "@/lib/utils"

type DemoStatus = "ready" | "running" | "complete"

type DemoLogEntry = {
  time: string
  message: string
}

type ResourcePoint = {
  time: string
  cpu: number
  gpu: number
  ram: number
}

const DEMO_DURATION_MS = 10_000
const TOTAL_BARS = 64

const SAMPLE_HISTORY: ResourcePoint[] = [
  { time: "−4.0s", cpu: 22, gpu: 14, ram: 31 },
  { time: "−3.5s", cpu: 25, gpu: 18, ram: 32 },
  { time: "−3.0s", cpu: 24, gpu: 21, ram: 32 },
  { time: "−2.5s", cpu: 29, gpu: 24, ram: 33 },
  { time: "−2.0s", cpu: 31, gpu: 28, ram: 34 },
  { time: "−1.5s", cpu: 27, gpu: 32, ram: 34 },
  { time: "−1.0s", cpu: 34, gpu: 35, ram: 35 },
  { time: "−0.5s", cpu: 32, gpu: 39, ram: 35 },
  { time: "0.0s", cpu: 36, gpu: 42, ram: 36 },
]

const DEMO_LOG_STEPS = [
  { at: 0, message: "Khởi tạo tác vụ voice_demo_042 · cấu hình vi-VN" },
  { at: 850, message: "Đọc mẫu giọng · voice_sample_vi.wav · 12,4 MB" },
  { at: 2_050, message: "Khử nhiễu nền và cân bằng âm lượng −14 LUFS" },
  { at: 3_500, message: "Trích xuất đặc trưng âm sắc OmniVoice FP16" },
  { at: 5_150, message: "Tạo embedding cá nhân cho giọng Minh An" },
  { at: 7_050, message: "Tổng hợp waveform bản xem trước 24 kHz" },
  { at: 8_750, message: "Kiểm tra chất lượng · độ khớp mẫu 94/100" },
  { at: 10_000, message: "Hoàn tất · voice_demo_042 đã sẵn sàng sử dụng" },
]

const PROCESS_STAGES = [
  { progress: 0, label: "Khởi tạo tác vụ" },
  { progress: 14, label: "Phân tích mẫu âm thanh" },
  { progress: 34, label: "Trích xuất đặc trưng" },
  { progress: 53, label: "Tạo embedding giọng" },
  { progress: 72, label: "Tổng hợp waveform" },
  { progress: 90, label: "Kiểm tra chất lượng" },
  { progress: 100, label: "Hoàn tất" },
]

const waveformHeights = Array.from({ length: TOTAL_BARS }, (_, index) => {
  const position = index / (TOTAL_BARS - 1)
  const window = 0.25 + 0.75 * Math.sin(position * Math.PI)
  const cadence =
    Math.abs(Math.sin(index * 0.48) * 0.45) +
    Math.abs(Math.cos(index * 1.15) * 0.35) +
    Math.abs(Math.sin(index * 2.3) * 0.2)
  return Math.max(14, Math.min(96, Math.round(14 + window * cadence * 82)))
})

const resourceChartConfig = {
  cpu: { label: "CPU", color: "var(--chart-1)" },
  gpu: { label: "GPU", color: "var(--chart-2)" },
} satisfies ChartConfig

function formatElapsed(milliseconds: number) {
  const seconds = Math.floor(milliseconds / 1000)
  const tenths = Math.floor((milliseconds % 1000) / 100)
  return `00:${String(seconds).padStart(2, "0")}.${tenths}`
}

function formatChartTime(milliseconds: number) {
  return `${(milliseconds / 1000).toFixed(1)}s`
}

function createResourcePoint(milliseconds: number): ResourcePoint {
  const seconds = milliseconds / 1000
  const progress = (milliseconds / DEMO_DURATION_MS) * 100
  const clamp = (value: number) => Math.max(8, Math.min(92, Math.round(value)))

  return {
    time: formatChartTime(milliseconds),
    cpu: clamp(31 + Math.sin(seconds * 1.2) * 13 + progress * 0.16),
    gpu: clamp(27 + Math.sin(seconds * 0.9 + 0.8) * 22 + progress * 0.2),
    ram: clamp(35 + Math.sin(seconds * 0.45) * 3 + progress * 0.11),
  }
}

function ResourceStat({
  icon: Icon,
  label,
  value,
  colorClass,
}: {
  icon: LucideIcon
  label: string
  value: string
  colorClass: string
}) {
  return (
    <div className="rounded-lg border border-border/70 bg-background/80 px-2.5 py-1.5 shadow-2xs">
      <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground">
        <Icon className="size-3" aria-hidden="true" />
        <span>{label}</span>
      </div>
      <p className={cn("mt-0.5 text-[13px] font-semibold tabular-nums tracking-tight", colorClass)}>
        {value}
      </p>
    </div>
  )
}

function WaveformPreview({ progress, isRunning }: { progress: number; isRunning: boolean }) {
  const completedBars = Math.round((progress / 100) * waveformHeights.length)

  return (
    <section className="rounded-xl border border-border/70 bg-muted/20 p-3.5" aria-label="Waveform demo">
      <div className="flex items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <AudioLines className="size-4 shrink-0 text-primary" aria-hidden="true" />
          <div className="min-w-0">
            <h4 className="truncate text-[11px] font-semibold text-foreground">Waveform bản xem trước</h4>
            <p className="mt-0.5 truncate text-[10px] text-muted-foreground">
              Minh An · Mẫu giọng tiếng Việt · 12,4 giây · Chuẩn phòng thu 24 kHz
            </p>
          </div>
        </div>
        <span className="shrink-0 font-mono text-[10px] tabular-nums text-muted-foreground">
          {Math.round(progress)}%
        </span>
      </div>

      <div
        role="img"
        aria-label={`Waveform demo, ${Math.round(progress)} phần trăm đã xử lý`}
        data-playing={isRunning}
        className="relative mt-3 flex h-[78px] items-center overflow-hidden rounded-lg border border-border/70 bg-background/90 px-3 py-2 shadow-inner"
      >
        <div className="flex h-full w-full items-center justify-between gap-[2px]">
          {waveformHeights.map((height, index) => (
            <span
              key={index}
              className={cn(
                "waveform-bar min-h-1 flex-1 rounded-full transition-colors duration-150",
                index < completedBars ? "bg-primary" : "bg-muted-foreground/20"
              )}
              style={{
                height: `${height}%`,
                animationDelay: `${(index % 14) * 35}ms`,
              }}
            />
          ))}
        </div>
        <span
          aria-hidden="true"
          className="pointer-events-none absolute inset-y-1 w-0.5 rounded-full bg-primary shadow-[0_0_8px_var(--primary)] transition-[left] duration-100 ease-linear"
          style={{ left: `${Math.min(99, Math.max(1, progress))}%` }}
        />
      </div>

      <div className="mt-2.5 flex items-center justify-between gap-3 text-[10px] font-mono text-muted-foreground">
        <span>
          {isRunning ? "Đang dựng waveform realtime" : progress === 100 ? "Waveform đã hoàn tất" : "Waveform mẫu"}
        </span>
        <span className="tabular-nums">
          {formatElapsed(progress === 100 ? DEMO_DURATION_MS : (progress / 100) * DEMO_DURATION_MS)} / 00:10.0
        </span>
      </div>
      <div
        role="progressbar"
        aria-label="Tiến trình tạo voice demo"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={Math.round(progress)}
        aria-valuetext={`${Math.round(progress)}% · ${progress === 100 ? "Hoàn tất" : "Đang xử lý"}`}
        className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted"
      >
        <div
          className="h-full rounded-full bg-primary transition-[width] duration-150 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
    </section>
  )
}

function DemoLogPanel({
  status,
  logs,
  logContainerRef,
}: {
  status: DemoStatus
  logs: DemoLogEntry[]
  logContainerRef: React.RefObject<HTMLDivElement | null>
}) {
  return (
    <section className="min-w-0 rounded-xl border border-border/70 bg-card p-3.5 shadow-2xs" aria-label="Nhật ký realtime">
      <div className="flex items-center justify-between gap-3 border-b border-border/60 pb-2.5">
        <div className="flex items-center gap-2">
          <Terminal className="size-3.5 text-muted-foreground" aria-hidden="true" />
          <h4 className="text-[11px] font-semibold text-foreground">Nhật ký tiến trình</h4>
        </div>
        <span className="flex shrink-0 items-center gap-1.5 text-[9px] text-muted-foreground">
          <span
            className={cn(
              "size-1.5 rounded-full",
              status === "running" ? "bg-primary motion-safe:animate-pulse" : "bg-muted-foreground/45"
            )}
          />
          {status === "running" ? "Theo dõi trực tiếp" : status === "complete" ? "Đã hoàn tất" : "Sẵn sàng"}
        </span>
      </div>

      <div
        ref={logContainerRef}
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        className="mt-3 max-h-[220px] min-h-[175px] overflow-y-auto rounded-lg border border-border/50 bg-muted/20 p-2.5 font-mono"
      >
        {logs.length > 0 ? (
          <ol className="flex flex-col gap-2">
            {logs.map((entry, idx) => (
              <li key={idx} className="flex items-start gap-2 text-[10px] leading-4">
                <Check className="mt-0.5 size-3 shrink-0 text-primary" aria-hidden="true" />
                <time className="shrink-0 tabular-nums text-muted-foreground">{entry.time}</time>
                <span className="min-w-0 font-sans text-foreground/85">{entry.message}</span>
              </li>
            ))}
          </ol>
        ) : (
          <div className="flex min-h-[150px] flex-col items-center justify-center gap-2 px-3 text-center">
            <Activity className="size-4 text-muted-foreground/70" aria-hidden="true" />
            <p className="max-w-[250px] text-[10px] leading-4 text-muted-foreground">
              Nhấn “Chạy demo” để quan sát từng bước tạo giọng xuất hiện theo thời gian thực.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}

function ResourceUsagePanel({ history, status }: { history: ResourcePoint[]; status: DemoStatus }) {
  const current = history[history.length - 1] ?? SAMPLE_HISTORY[SAMPLE_HISTORY.length - 1]
  const memoryGb = ((current.ram / 100) * 8).toFixed(1)

  return (
    <section className="min-w-0 rounded-xl border border-border/70 bg-card p-3.5 shadow-2xs" aria-label="Tài nguyên máy mô phỏng">
      <div className="flex items-start justify-between gap-2 border-b border-border/60 pb-2.5">
        <div>
          <div className="flex items-center gap-1.5">
            <Cpu className="size-3.5 text-muted-foreground" aria-hidden="true" />
            <h4 className="text-[11px] font-semibold text-foreground">Tài nguyên máy</h4>
          </div>
          <p className="mt-0.5 text-[9px] text-muted-foreground">Mức dùng trong tác vụ demo</p>
        </div>
        <span className="rounded-md border border-primary/25 bg-primary/10 px-1.5 py-0.5 text-[9px] font-medium text-primary">
          Mô phỏng — không đọc tài nguyên máy thật
        </span>
      </div>

      <div className="mt-3 grid grid-cols-2 gap-2">
        <ResourceStat icon={Cpu} label="CPU" value={`${current.cpu}%`} colorClass="text-chart-1" />
        <ResourceStat icon={Activity} label="GPU" value={`${current.gpu}%`} colorClass="text-chart-2" />
      </div>

      <div className="mt-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-1.5 text-[9px] text-muted-foreground">
          <span className="size-1.5 rounded-full bg-chart-1" />CPU
          <span className="ml-1 size-1.5 rounded-full bg-chart-2" />GPU
        </div>
        <span className="text-[9px] text-muted-foreground">
          {status === "running" ? "Lịch sử realtime" : status === "complete" ? "Phiên hoàn tất" : "Dữ liệu mẫu"}
        </span>
      </div>
      <ChartContainer config={resourceChartConfig} className="mt-1 h-[126px] min-h-0 w-full aspect-auto">
        <LineChart accessibilityLayer data={history} margin={{ top: 8, right: 5, bottom: 0, left: -22 }}>
          <CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            axisLine={false}
            tickLine={false}
            tickMargin={6}
            minTickGap={20}
            tick={{ fontSize: 9 }}
          />
          <YAxis
            domain={[0, 100]}
            ticks={[0, 50, 100]}
            axisLine={false}
            tickLine={false}
            width={30}
            tickFormatter={(value: number) => `${value}%`}
            tick={{ fontSize: 9 }}
          />
          <ChartTooltip
            cursor={false}
            content={
              <ChartTooltipContent
                hideLabel
                indicator="line"
                formatter={(value, name) => [`${value}%`, name]}
              />
            }
          />
          <Line
            type="monotone"
            dataKey="cpu"
            stroke="var(--color-cpu)"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="gpu"
            stroke="var(--color-gpu)"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ChartContainer>

      <div className="mt-2 border-t border-border/60 pt-2.5">
        <div className="flex items-center justify-between gap-3 text-[10px]">
          <span className="flex items-center gap-1.5 text-muted-foreground">
            <HardDrive className="size-3.5" aria-hidden="true" />RAM
          </span>
          <span className="font-mono font-medium tabular-nums text-foreground">{memoryGb} / 8.0 GB</span>
        </div>
        <div
          role="progressbar"
          aria-label="RAM mô phỏng"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={current.ram}
          aria-valuetext={`${memoryGb} trên 8 GB`}
          className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted"
        >
          <div
            className="h-full rounded-full bg-chart-3 transition-[width] duration-300 ease-out"
            style={{ width: `${current.ram}%` }}
          />
        </div>
      </div>
      <p className="mt-2.5 text-[9px] leading-4 text-muted-foreground">
        * Mô phỏng — không đọc tài nguyên máy thật.
      </p>
    </section>
  )
}

export function VoiceGenerationDemo({
  selectedVoiceId = "minh-an",
  onGenerated,
}: {
  selectedVoiceId?: string
  onGenerated?: () => void
} = {}) {
  const [status, setStatus] = useState<DemoStatus>("ready")
  const [progress, setProgress] = useState(0)
  const [elapsed, setElapsed] = useState(0)
  const [logs, setLogs] = useState<DemoLogEntry[]>([])
  const [resourceHistory, setResourceHistory] = useState(SAMPLE_HISTORY)
  const logContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (status !== "running") return

    const startedAt = performance.now()
    let logIndex = 0
    let lastSampleAt = -Number.POSITIVE_INFINITY

    const intervalId = window.setInterval(() => {
      const nextElapsed = Math.min(performance.now() - startedAt, DEMO_DURATION_MS)
      const nextProgress = (nextElapsed / DEMO_DURATION_MS) * 100
      setElapsed(nextElapsed)
      setProgress(nextProgress)

      const newEntries: DemoLogEntry[] = []
      while (logIndex < DEMO_LOG_STEPS.length && DEMO_LOG_STEPS[logIndex].at <= nextElapsed) {
        const step = DEMO_LOG_STEPS[logIndex]
        newEntries.push({ time: formatElapsed(step.at), message: step.message })
        logIndex += 1
      }
      if (newEntries.length > 0) {
        setLogs((currentLogs) => [...currentLogs, ...newEntries])
      }

      if (nextElapsed - lastSampleAt >= 320 || nextElapsed === DEMO_DURATION_MS) {
        setResourceHistory((currentHistory) => [...currentHistory.slice(-23), createResourcePoint(nextElapsed)])
        lastSampleAt = nextElapsed
      }

      if (nextElapsed >= DEMO_DURATION_MS) {
        setStatus("complete")
        onGenerated?.()
      }
    }, 100)

    return () => window.clearInterval(intervalId)
  }, [status, onGenerated])

  useEffect(() => {
    if (logs.length > 0 && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }, [logs])

  const currentStage = useMemo(() => {
    return PROCESS_STAGES.reduce(
      (activeStage, stage) => (progress >= stage.progress ? stage : activeStage),
      PROCESS_STAGES[0]
    )
  }, [progress])

  const statusLabel = status === "running" ? "Đang tạo voice" : status === "complete" ? "Đã hoàn tất" : "Sẵn sàng"

  function startDemo() {
    setStatus("running")
    setProgress(0)
    setElapsed(0)
    setLogs([])
    setResourceHistory(SAMPLE_HISTORY.slice(-7))
  }

  return (
    <Card className="mb-4 gap-0 overflow-hidden rounded-2xl border-border/80 bg-card py-0 shadow-sm">
      <CardHeader className="grid-cols-[minmax(0,1fr)_auto] gap-x-3 gap-y-1.5 border-b border-border/70 bg-muted/20 px-4 py-3 sm:px-5">
        <CardTitle className="flex min-w-0 items-center gap-2 text-[12px] font-semibold tracking-tight text-foreground sm:text-[13px]">
          <span className="flex size-7 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <Sparkles className="size-3.5" aria-hidden="true" />
          </span>
          <span className="truncate">Demo tạo voice realtime</span>
        </CardTitle>
        <CardAction className="mt-0">
          <Button
            type="button"
            variant={status === "running" ? "secondary" : "default"}
            size="sm"
            onClick={startDemo}
            disabled={status === "running"}
            className="h-8 rounded-lg px-3 text-[11px] font-medium shadow-2xs"
          >
            {status === "running" ? (
              <LoaderCircle className="size-3.5 motion-safe:animate-spin" data-icon="inline-start" aria-hidden="true" />
            ) : status === "complete" ? (
              <RotateCcw className="size-3.5" data-icon="inline-start" aria-hidden="true" />
            ) : (
              <Play className="size-3.5 fill-current" data-icon="inline-start" aria-hidden="true" />
            )}
            {status === "running" ? "Đang chạy..." : status === "complete" ? "Chạy lại" : "Chạy demo"}
          </Button>
        </CardAction>
        <CardDescription className="col-span-2 text-[10px] leading-4 text-muted-foreground sm:text-[11px]">
          Mô phỏng tạo giọng “Minh An” · Mẫu 12,4 giây · Không cần tải tệp lên.
        </CardDescription>
      </CardHeader>

      <CardContent className="flex flex-col gap-3.5 p-3.5 sm:p-4.5">
        <div className="flex items-center justify-between gap-3">
          <p className="flex min-w-0 items-center gap-2 text-[10px] font-medium text-muted-foreground" role="status" aria-live="polite">
            <span
              className={cn(
                "size-1.5 shrink-0 rounded-full",
                status === "running" ? "bg-primary motion-safe:animate-pulse" : status === "complete" ? "bg-primary" : "bg-muted-foreground/45"
              )}
            />
            <span className="truncate">
              {statusLabel} · {status === "running" ? currentStage.label : status === "complete" ? "voice_demo_042 sẵn sàng" : "Dữ liệu mẫu đã nạp"}
            </span>
          </p>
          <span className="shrink-0 font-mono text-[10px] tabular-nums text-muted-foreground">
            {formatElapsed(elapsed)} / 00:10.0
          </span>
        </div>

        <WaveformPreview progress={progress} isRunning={status === "running"} />

        <div className="grid gap-3 xl:grid-cols-[minmax(0,1.15fr)_minmax(260px,0.85fr)]">
          <DemoLogPanel status={status} logs={logs} logContainerRef={logContainerRef} />
          <ResourceUsagePanel history={resourceHistory} status={status} />
        </div>
      </CardContent>
    </Card>
  )
}
