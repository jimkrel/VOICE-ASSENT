"use client"

import { AudioLines, Mic, Wand2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { TOOL_LABELS, type WorkspaceTool } from "@/components/workspace-sidebar"

export function WorkspacePlaceholder({
  activeTool,
  onSelect,
}: {
  activeTool: WorkspaceTool
  onSelect: (tool: WorkspaceTool) => void
}) {
  return (
    <section className="flex min-h-[640px] items-center justify-center px-6 py-12" aria-label={TOOL_LABELS[activeTool]}>
      <div className="max-w-[520px] text-center">
        <span className="mx-auto mb-5 flex size-12 items-center justify-center rounded-2xl bg-[#f2f2f2] text-[#424242]">
          <AudioLines className="size-5" aria-hidden="true" />
        </span>
        <p className="text-[11px] font-medium uppercase tracking-[0.12em] text-[#858585]">
          Không gian Thành Âm
        </p>
        <h2 className="mt-2 text-2xl font-medium tracking-tight text-[#181818]">
          {TOOL_LABELS[activeTool]}
        </h2>
        <p className="mt-3 text-sm leading-6 text-[#737373]">
          Khung điều hướng đã sẵn sàng. Bản xem trước hiện tập trung vào ba luồng: chuyển văn bản, tạo giọng đọc và đổi giọng.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => onSelect("text-to-speech")}
            className="rounded-lg border-[#dedede]"
          >
            <AudioLines data-icon="inline-start" />
            Chuyển văn bản
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => onSelect("voice-creation")}
            className="rounded-lg border-[#dedede]"
          >
            <Mic data-icon="inline-start" />
            Tạo giọng đọc
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => onSelect("voice-changer")}
            className="rounded-lg border-[#dedede]"
          >
            <Wand2 data-icon="inline-start" />
            Đổi giọng
          </Button>
        </div>
      </div>
    </section>
  )
}
