"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  AudioLines,
  LayoutGrid,
  Mic,
  RefreshCw,
} from "lucide-react"
import type { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

export type WorkspaceTool =
  | "text-to-speech"
  | "voice-creation"
  | "voice-changer"
  | "voice-library"

export const TOOL_LABELS: Record<WorkspaceTool, string> = {
  "text-to-speech": "Đọc kịch bản",
  "voice-creation": "Tạo giọng mới",
  "voice-changer": "Đổi giọng",
  "voice-library": "Kho giọng đọc",
}

export type NavigationItem = {
  id: WorkspaceTool
  href: string
  label: string
  icon: LucideIcon
}

export const navigationItems: NavigationItem[] = [
  { id: "text-to-speech", href: "/text-to-speech", label: "Đọc kịch bản", icon: AudioLines },
  { id: "voice-creation", href: "/voice-creation", label: "Tạo giọng mới", icon: Mic },
  { id: "voice-changer", href: "/voice-changer", label: "Đổi giọng", icon: RefreshCw },
  { id: "voice-library", href: "/voice-library", label: "Kho giọng đọc", icon: LayoutGrid },
]

const compactLabels: Record<WorkspaceTool, string> = {
  "text-to-speech": "Đọc",
  "voice-creation": "Tạo",
  "voice-changer": "Đổi",
  "voice-library": "Kho",
}

export function isToolActive(pathname: string, toolId: WorkspaceTool): boolean {
  if (pathname === `/${toolId}`) return true
  if (toolId === "text-to-speech" && (pathname === "/" || pathname === "")) return true
  return false
}

function NavigationLink({
  item,
}: {
  item: NavigationItem
}) {
  const pathname = usePathname()
  const isActive = isToolActive(pathname, item.id)
  const Icon = item.icon

  return (
    <Link
      href={item.href}
      aria-current={isActive ? "page" : undefined}
      className={cn(
        "flex h-9 w-full items-center gap-2.5 rounded-lg px-2.5 text-left text-[12px] font-medium transition-colors",
        isActive
          ? "bg-primary/15 font-semibold text-primary"
          : "text-muted-foreground hover:bg-muted hover:text-foreground"
      )}
    >
      <Icon className="size-4 shrink-0" aria-hidden="true" />
      <span className="min-w-0 truncate">{item.label}</span>
    </Link>
  )
}

export function WorkspaceSidebar({
  searchValue = "",
}: {
  searchValue?: string
  activeTool?: WorkspaceTool
  onSelect?: (tool: WorkspaceTool) => void
}) {
  const query = searchValue.trim().toLocaleLowerCase("vi")
  const filteredItems = query
    ? navigationItems.filter((item) => item.label.toLocaleLowerCase("vi").includes(query))
    : navigationItems

  return (
    <aside
      aria-label="Điều hướng chính"
      className="hidden h-full w-[190px] shrink-0 flex-col border-r border-border bg-card lg:flex"
    >
      <Link
        href="/text-to-speech"
        className="mx-4 flex h-[56px] shrink-0 items-center gap-2.5 border-b border-border px-1 text-[14px] font-semibold tracking-[-0.025em] text-foreground hover:opacity-90"
      >
        <span className="flex size-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <AudioLines className="size-3.5" aria-hidden="true" />
        </span>
        <span>Thành Âm</span>
      </Link>

      <div className="px-3.5 pt-5">
        <p className="px-2 text-[10px] font-semibold uppercase tracking-[0.09em] text-muted-foreground">
          Không gian làm việc
        </p>
        <nav aria-label="Công cụ giọng nói" className="mt-3 flex flex-col gap-1">
          {filteredItems.map((item) => (
            <NavigationLink
              key={item.id}
              item={item}
            />
          ))}
        </nav>
        {query && filteredItems.length === 0 ? (
          <p className="px-2 py-4 text-xs leading-5 text-muted-foreground">
            Không tìm thấy công cụ phù hợp.
          </p>
        ) : null}
      </div>
    </aside>
  )
}

export function WorkspaceMobileNav({
  activeTool,
  onSelect,
}: {
  activeTool?: WorkspaceTool
  onSelect?: (tool: WorkspaceTool) => void
} = {}) {
  const pathname = usePathname()

  return (
    <nav
      aria-label="Công cụ chính"
      className="grid shrink-0 grid-cols-4 gap-1 border-b border-border bg-card px-2 py-2 lg:hidden"
    >
      {navigationItems.map((item) => {
        const Icon = item.icon
        const isActive = activeTool ? activeTool === item.id : isToolActive(pathname, item.id)

        return (
          <Link
            key={item.id}
            href={item.href}
            onClick={() => onSelect?.(item.id)}
            aria-label={item.label}
            title={item.label}
            aria-current={isActive ? "page" : undefined}
            className={cn(
              "flex h-9 min-w-0 items-center justify-center gap-1 rounded-lg px-1.5 text-[11px] font-medium transition-colors",
              isActive
                ? "bg-primary/15 font-semibold text-primary"
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            )}
          >
            <Icon className="size-3.5 shrink-0" aria-hidden="true" />
            <span className="truncate">{compactLabels[item.id]}</span>
          </Link>
        )
      })}
    </nav>
  )
}
