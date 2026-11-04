"use client"

import { useEffect, useState } from "react"
import { usePathname } from "next/navigation"
import { useTheme } from "next-themes"
import { Activity, AudioLines, Cpu, HardDrive, Moon, Search, SlidersHorizontal, Sun, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { TOOL_LABELS, type WorkspaceTool } from "@/components/workspace-sidebar"
import { useVoiceStudio } from "@/components/voice-studio-context"

function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const isDark = mounted && resolvedTheme === "dark"

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <Button
      type="button"
      variant="ghost"
      size="icon-sm"
      aria-label={isDark ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối"}
      aria-pressed={isDark}
      title={isDark ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối"}
      onClick={() => setTheme(isDark ? "light" : "dark")}
      className="rounded-lg text-muted-foreground hover:text-foreground"
    >
      {isDark ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
    </Button>
  )
}

export function WorkspaceTopBar({
  activeTool: propActiveTool,
  searchValue,
  onSearchChange,
  onToggleMobileSettings,
  mobileSettingsOpen,
  showSettings,
}: {
  activeTool?: WorkspaceTool
  searchValue: string
  onSearchChange: (value: string) => void
  onToggleMobileSettings?: () => void
  mobileSettingsOpen?: boolean
  showSettings?: boolean
}) {
  const pathname = usePathname()
  const { telemetry } = useVoiceStudio()

  const activeTool: WorkspaceTool =
    propActiveTool ||
    (pathname.includes("voice-creation")
      ? "voice-creation"
      : pathname.includes("voice-changer")
        ? "voice-changer"
        : pathname.includes("voice-library")
          ? "voice-library"
          : "text-to-speech")

  return (
    <header className="relative flex h-[52px] shrink-0 items-center justify-between gap-2.5 border-b border-border bg-card px-3.5 sm:px-5">
      {/* Left: Brand/Tool Title */}
      <div className="flex min-w-0 items-center gap-2.5">
        <span className="flex size-7 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground lg:hidden">
          <AudioLines className="size-3.5" aria-hidden="true" />
        </span>
        <h1 className="max-w-[170px] truncate text-[13px] font-semibold tracking-[-0.01em] text-foreground sm:max-w-[220px]">
          {TOOL_LABELS[activeTool]}
        </h1>
      </div>

      {/* Middle: Real Machine Hardware Telemetry */}
      <div className="flex items-center gap-2">
        <div
          className="flex items-center gap-2.5 rounded-lg border border-border bg-muted/60 px-2.5 py-1 text-[11px] font-mono text-muted-foreground shadow-2xs"
          title={`Phần cứng thật: ${telemetry.gpuName} | Nhiệt độ GPU: ${telemetry.gpuTemp}°C`}
        >
          {/* GPU & VRAM */}
          <div className="flex items-center gap-1.5">
            <span
              className={`size-2 shrink-0 rounded-full ${
                telemetry.gpu > 80 ? "bg-amber-500 animate-ping" : "bg-emerald-500 animate-pulse"
              }`}
            />
            <span className="font-semibold text-foreground">GPU:</span>
            <span>{telemetry.gpu}%</span>
            <span className="hidden text-[10px] text-muted-foreground/80 sm:inline">
              ({telemetry.gpuTemp}°C)
            </span>
            <span className="text-muted-foreground/40">|</span>
            <span className="font-semibold text-foreground">VRAM:</span>
            <span>
              {telemetry.vramUsedGb}/{telemetry.vramTotalGb}GB
            </span>
          </div>

          <div className="hidden h-3 w-px bg-border md:block" />

          {/* CPU & RAM */}
          <div className="hidden items-center gap-1.5 md:flex">
            <span className="font-semibold text-foreground">CPU:</span>
            <span>{telemetry.cpu}%</span>
            <span className="text-muted-foreground/40">|</span>
            <span className="font-semibold text-foreground">RAM:</span>
            <span>
              {telemetry.ramUsedGb}/{telemetry.ramTotalGb}GB
            </span>
          </div>
        </div>
      </div>

      {/* Right: Search + Theme + Settings Button */}
      <div className="flex shrink-0 items-center gap-2">
        <label className="hidden h-8 w-[180px] items-center gap-2 rounded-lg border border-border bg-muted px-2.5 text-muted-foreground focus-within:border-ring focus-within:ring-2 focus-within:ring-ring/25 xl:flex">
          <Search className="size-3.5 shrink-0" aria-hidden="true" />
          <input
            type="search"
            value={searchValue}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Tìm kiếm..."
            aria-label="Tìm kiếm công cụ"
            className="min-w-0 flex-1 bg-transparent text-[11px] text-foreground outline-none placeholder:text-muted-foreground"
          />
        </label>

        <ThemeToggle />

        {showSettings && onToggleMobileSettings ? (
          <Button
            type="button"
            variant={mobileSettingsOpen ? "secondary" : "outline"}
            size="sm"
            aria-expanded={mobileSettingsOpen}
            onClick={onToggleMobileSettings}
            className="h-8 gap-1.5 rounded-lg border-border px-2.5 text-[11px] font-medium xl:hidden"
          >
            <SlidersHorizontal data-icon="inline-start" />
            {mobileSettingsOpen ? "Ẩn cài đặt" : "Cài đặt"}
          </Button>
        ) : null}
      </div>
    </header>
  )
}

