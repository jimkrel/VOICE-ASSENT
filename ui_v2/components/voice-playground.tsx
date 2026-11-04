"use client"

import { useState } from "react"
import Image from "next/image"
import {
  ArrowRight,
  ArrowUpRight,
  AudioLines,
  Check,
  Code2,
  Copy,
  Headphones,
  Pause,
  Play,
  Sparkles,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"

const waveformHeights = [
  24, 42, 34, 60, 44, 76, 38, 56, 88, 50, 34, 66, 92, 58, 38, 72, 48, 82,
  42, 62, 94, 54, 32, 70, 46, 84, 58, 36, 74, 48, 90, 60, 40, 68, 96, 52,
  36, 78, 46, 64, 88, 54, 34, 72, 48, 82, 58, 38, 68, 92, 46, 62,
]

const sampleCode = `const banNghe = await thanhAm.taoGiongNoi({
  vanBan: "Xin chào, chúc bạn một ngày nhiều cảm hứng.",
  giongDoc: "minh-anh",
})`

function Waveform({ active }: { active: boolean }) {
  return (
    <div
      aria-hidden="true"
      className="flex h-8 flex-1 items-center gap-[3px] overflow-hidden"
      data-playing={active}
    >
      {waveformHeights.map((height, index) => (
        <span
          className="waveform-bar w-[3px] shrink-0 rounded-full bg-[#9a765b]"
          key={`${height}-${index}`}
          style={{ height: `${height}%`, animationDelay: `${index * 24}ms` }}
        />
      ))}
    </div>
  )
}

function AudioPreviewCard({
  isPlaying,
  onToggle,
  voiceName,
  voiceDescription,
}: {
  isPlaying: boolean
  onToggle: () => void
  voiceName: string
  voiceDescription: string
}) {
  return (
    <div className="relative isolate min-h-[410px] overflow-hidden bg-[#eeeae3]">
      <Image
        alt=""
        className="object-cover"
        fill
        sizes="(max-width: 1024px) 100vw, 45vw"
        src="/voice-orbs.png"
          loading="eager"
      />
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-gradient-to-b from-white/15 via-transparent to-[#211e1b]/30"
      />
      <div className="relative flex min-h-[410px] flex-col justify-between p-5 sm:p-7">
        <div className="inline-flex w-fit items-center gap-2 rounded-full border border-white/70 bg-white/70 px-3.5 py-2 text-xs font-medium text-[#51483f] shadow-sm backdrop-blur-md">
          <Sparkles aria-hidden="true" className="size-3.5 text-[#a66e4d]" />
          Bản xem trước tương tác
        </div>

        <div className="rounded-[22px] border border-white/70 bg-white/90 p-4 shadow-[0_16px_50px_rgba(35,28,22,0.16)] backdrop-blur-xl sm:p-5">
          <div className="flex items-center gap-3">
            <span className="grid size-11 shrink-0 place-items-center rounded-full bg-[#eee4da] text-[#73583f]">
              <AudioLines aria-hidden="true" className="size-[18px]" />
            </span>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-[#211f1c]">
                {voiceName}
              </p>
              <p className="mt-0.5 truncate text-xs text-[#7c746b]">
                {voiceDescription}
              </p>
            </div>
            <Button
              aria-label={isPlaying ? "Tạm dừng mô phỏng" : "Bật mô phỏng giọng nói"}
              aria-pressed={isPlaying}
              className="rounded-full"
              onClick={onToggle}
              size="icon-lg"
              type="button"
            >
              {isPlaying ? (
                <Pause aria-hidden="true" />
              ) : (
                <Play aria-hidden="true" />
              )}
            </Button>
          </div>

          <div className="mt-4 flex items-center gap-3">
            <span className="text-[10px] tabular-nums text-[#777067]">00:00</span>
            <Waveform active={isPlaying} />
            <span className="text-[10px] tabular-nums text-[#777067]">00:08</span>
          </div>
          <div
            aria-live="polite"
            className="mt-2 text-[11px] text-[#79736b]"
            role="status"
          >
            {isPlaying ? "Mô phỏng đang chạy" : "Mô phỏng phát giọng nói"}
          </div>
        </div>
      </div>
    </div>
  )
}

function CreativePanel({
  isPlaying,
  onToggle,
}: {
  isPlaying: boolean
  onToggle: () => void
}) {
  const [previewReady, setPreviewReady] = useState(false)

  return (
    <div className="grid overflow-hidden rounded-[30px] border border-[#e7e3dd] bg-white shadow-[0_18px_65px_rgba(35,30,24,0.06)] lg:grid-cols-[1.04fr_0.96fr]">
      <div className="p-6 sm:p-8 lg:p-10">
        <div className="flex items-center gap-2.5">
          <span className="grid size-8 place-items-center rounded-full bg-[#eee5dc] text-[11px] font-semibold text-[#795d46]">
            01
          </span>
          <span className="text-[10px] font-semibold tracking-[0.16em] text-[#8b8176] sm:text-[11px]">
            CHUYỂN VĂN BẢN THÀNH GIỌNG NÓI
          </span>
        </div>
        <h3 className="mt-6 max-w-[430px] text-3xl font-medium leading-[1.1] tracking-[-0.055em] text-[#201e1b] sm:text-[2.5rem]">
          Giọng đọc rõ ràng, giàu cảm xúc.
        </h3>
        <p className="mt-3 max-w-[440px] text-sm leading-6 text-[#777067] sm:text-[15px]">
          Biến từng câu chữ thành lời kể tự nhiên, với nhịp điệu gần gũi như
          chính bạn đang trò chuyện.
        </p>

        <div className="mt-7 rounded-[20px] border border-[#eeeae4] bg-[#fbfaf8] p-4 sm:p-5">
          <p className="text-[10px] font-semibold tracking-[0.14em] text-[#9a8d80]">
            VĂN BẢN MẪU
          </p>
          <p className="mt-2.5 text-sm leading-6 text-[#4e4943] sm:text-[15px]">
            “Xin chào! Hãy cùng khám phá những ý tưởng mới và biến chúng thành
            trải nghiệm đáng nhớ.”
          </p>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-3">
          <div className="rounded-2xl border border-[#eeeae4] px-4 py-3">
            <p className="text-[10px] text-[#968d83]">Giọng đọc</p>
            <p className="mt-1 text-xs font-medium text-[#35312d] sm:text-sm">
              Minh Anh · Nữ miền Bắc
            </p>
          </div>
          <div className="rounded-2xl border border-[#eeeae4] px-4 py-3">
            <p className="text-[10px] text-[#968d83]">Sắc thái</p>
            <p className="mt-1 text-xs font-medium text-[#35312d] sm:text-sm">
              Ấm áp, tự nhiên
            </p>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center">
          <Button
            className="h-11 rounded-full px-5"
            onClick={() => setPreviewReady(true)}
            type="button"
          >
            Tạo bản xem thử
            <ArrowUpRight aria-hidden="true" data-icon="inline-end" />
          </Button>
          <p
            aria-live="polite"
            className="text-xs leading-5 text-[#827a70]"
            role="status"
          >
            {previewReady
              ? "Bản xem thử đã sẵn sàng trong giao diện minh họa."
              : "Đang xem trước giao diện phòng thu."}
          </p>
        </div>
      </div>

      <AudioPreviewCard
        isPlaying={isPlaying}
        onToggle={onToggle}
        voiceDescription="Nữ miền Bắc · Ấm áp, tự nhiên"
        voiceName="Minh Anh"
      />
    </div>
  )
}

function AgentPanel({
  isPlaying,
  onToggle,
}: {
  isPlaying: boolean
  onToggle: () => void
}) {
  const [showFollowUp, setShowFollowUp] = useState(false)

  return (
    <div className="grid overflow-hidden rounded-[30px] border border-[#e7e3dd] bg-white shadow-[0_18px_65px_rgba(35,30,24,0.06)] lg:grid-cols-[1.04fr_0.96fr]">
      <div className="p-6 sm:p-8 lg:p-10">
        <div className="flex items-center gap-2.5">
          <span className="grid size-8 place-items-center rounded-full bg-[#e6e9e2] text-[#5d684f]">
            <Headphones aria-hidden="true" className="size-4" />
          </span>
          <span className="text-[10px] font-semibold tracking-[0.16em] text-[#8b8176] sm:text-[11px]">
            TRỢ LÝ HỘI THOẠI
          </span>
        </div>
        <h3 className="mt-6 max-w-[430px] text-3xl font-medium leading-[1.1] tracking-[-0.055em] text-[#201e1b] sm:text-[2.5rem]">
          Cuộc trò chuyện tự nhiên, mọi lúc.
        </h3>
        <p className="mt-3 max-w-[440px] text-sm leading-6 text-[#777067] sm:text-[15px]">
          Tạo trợ lý giọng nói biết lắng nghe, phản hồi nhanh và giữ đúng sắc
          thái thương hiệu của bạn.
        </p>

        <div className="mt-7 rounded-[22px] border border-[#eeeae4] bg-[#fbfaf8] p-4 sm:p-5">
          <div className="flex justify-end">
            <p className="max-w-[86%] rounded-[18px] rounded-br-md bg-[#eae5df] px-4 py-3 text-sm leading-5 text-[#4c453e]">
              Mình muốn đổi lịch hẹn sang sáng mai.
            </p>
          </div>
          <div className="mt-3 flex items-start gap-2.5">
            <span className="mt-0.5 grid size-7 shrink-0 place-items-center rounded-full bg-[#e8ded3] text-[#70543b]">
              <AudioLines aria-hidden="true" className="size-3.5" />
            </span>
            <div className="max-w-[88%] rounded-[18px] rounded-tl-md border border-[#eee9e1] bg-white px-4 py-3 text-sm leading-5 text-[#4c453e]">
              Được chứ. Bạn muốn khoảng 9 giờ hay 10 giờ?
              {showFollowUp && (
                <p className="mt-2 border-t border-[#eeeae4] pt-2 text-xs leading-5 text-[#847a70]">
                  Trợ lý đã ghi nhận lựa chọn và sẵn sàng hỗ trợ bước tiếp theo.
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center">
          <Button
            className="h-11 rounded-full px-5"
            onClick={() => setShowFollowUp((isVisible) => !isVisible)}
            type="button"
            variant="outline"
          >
            {showFollowUp ? "Ẩn phản hồi tiếp theo" : "Xem phản hồi tiếp theo"}
            <ArrowRight aria-hidden="true" data-icon="inline-end" />
          </Button>
          <p aria-live="polite" className="text-xs text-[#827a70]" role="status">
            Hội thoại minh họa bằng tiếng Việt.
          </p>
        </div>
      </div>

      <AudioPreviewCard
        isPlaying={isPlaying}
        onToggle={onToggle}
        voiceDescription="Trợ lý giọng nói · Phản hồi tự nhiên"
        voiceName="Trợ lý Thành Âm"
      />
    </div>
  )
}

function DeveloperPanel({
  isPlaying,
  onToggle,
}: {
  isPlaying: boolean
  onToggle: () => void
}) {
  const [copyStatus, setCopyStatus] = useState("")

  async function handleCopyCode() {
    try {
      await navigator.clipboard.writeText(sampleCode)
      setCopyStatus("Đoạn mã đã được sao chép.")
    } catch {
      setCopyStatus("Trình duyệt hiện chưa cho phép sao chép đoạn mã.")
    }
  }

  return (
    <div className="grid overflow-hidden rounded-[30px] border border-[#e7e3dd] bg-white shadow-[0_18px_65px_rgba(35,30,24,0.06)] lg:grid-cols-[1.04fr_0.96fr]">
      <div className="p-6 sm:p-8 lg:p-10">
        <div className="flex items-center gap-2.5">
          <span className="grid size-8 place-items-center rounded-full bg-[#e5e8ec] text-[#536274]">
            <Code2 aria-hidden="true" className="size-4" />
          </span>
          <span className="text-[10px] font-semibold tracking-[0.16em] text-[#8b8176] sm:text-[11px]">
            DÀNH CHO NHÀ PHÁT TRIỂN
          </span>
        </div>
        <h3 className="mt-6 max-w-[430px] text-3xl font-medium leading-[1.1] tracking-[-0.055em] text-[#201e1b] sm:text-[2.5rem]">
          Giọng nói tự nhiên trong sản phẩm của bạn.
        </h3>
        <p className="mt-3 max-w-[440px] text-sm leading-6 text-[#777067] sm:text-[15px]">
          Kết nối khả năng tạo giọng nói vào ứng dụng, dịch vụ và quy trình nội
          dung hiện có.
        </p>

        <div className="mt-7 flex flex-col gap-3">
          {[
            "Gửi văn bản cần chuyển đổi",
            "Chọn chất giọng phù hợp",
            "Nhận âm thanh cho sản phẩm",
          ].map((step, index) => (
            <div className="flex items-center gap-3" key={step}>
              <span className="grid size-7 shrink-0 place-items-center rounded-full border border-[#e9e4de] text-[10px] font-semibold text-[#7a6d5f]">
                0{index + 1}
              </span>
              <span className="text-sm text-[#514c45]">{step}</span>
            </div>
          ))}
        </div>

        <AudioPreviewCard
          isPlaying={isPlaying}
          onToggle={onToggle}
          voiceDescription="Bản xem trước trong quy trình tích hợp"
          voiceName="Giọng nói tiếng Việt"
        />
      </div>

      <div className="flex min-h-full flex-col justify-center bg-[#1e1c19] p-6 text-white sm:p-8 lg:p-9">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-[10px] font-semibold tracking-[0.16em] text-white/50">
              MẪU TÍCH HỢP
            </p>
            <p className="mt-1.5 text-sm font-medium text-white/85">
              Tạo giọng nói bằng vài dòng lệnh
            </p>
          </div>
          <span className="rounded-full border border-white/15 px-2.5 py-1 text-[10px] text-white/60">
            Tiếng Việt
          </span>
        </div>

        <pre className="mt-6 overflow-x-auto rounded-[20px] border border-white/10 bg-[#151412] p-4 text-[11px] leading-6 text-[#e7c9ad] sm:p-5 sm:text-xs">
          <code>{sampleCode}</code>
        </pre>

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <Button
            className="h-10 rounded-full px-4"
            onClick={handleCopyCode}
            type="button"
            variant="outline"
          >
            {copyStatus.startsWith("Đoạn mã") ? (
              <Check aria-hidden="true" data-icon="inline-start" />
            ) : (
              <Copy aria-hidden="true" data-icon="inline-start" />
            )}
            Sao chép đoạn mã
          </Button>
          <p aria-live="polite" className="text-xs text-white/60" role="status">
            {copyStatus || "Mẫu minh họa tích hợp."}
          </p>
        </div>
      </div>
    </div>
  )
}

export function VoicePlayground() {
  const [isPlaying, setIsPlaying] = useState(false)
  const togglePlayback = () => setIsPlaying((isActive) => !isActive)

  return (
    <section
      aria-describedby="demo-description"
      aria-labelledby="demo-heading"
      className="px-5 pb-20 pt-2 sm:px-8 sm:pb-24 sm:pt-3 lg:px-10"
      id="demo"
    >
      <div className="mx-auto max-w-[1280px]">
        <h2 className="sr-only" id="demo-heading">
          Nghe thử điều bạn có thể tạo.
        </h2>
        <p className="sr-only" id="demo-description">
          Chọn một trải nghiệm để khám phá giao diện Thành Âm. Đây là bản minh họa, chưa kết nối dịch vụ tạo âm thanh.
        </p>

        <Tabs className="w-full" defaultValue="sang-tao">
          <TabsList
            aria-label="Chọn trải nghiệm"
            className="grid h-auto w-full grid-cols-3 rounded-[22px] bg-[#eeece8] p-1.5"
          >
            <TabsTrigger
              className="h-12 rounded-[17px] px-2 text-[12px] text-[#77716b] data-active:bg-white data-active:text-[#1c1a17] data-active:shadow-sm sm:px-4 sm:text-sm"
              value="sang-tao"
            >
              <AudioLines aria-hidden="true" data-icon="inline-start" />
              <span>Sáng tạo</span>
            </TabsTrigger>
            <TabsTrigger
              className="h-12 rounded-[17px] px-2 text-[12px] text-[#77716b] data-active:bg-white data-active:text-[#1c1a17] data-active:shadow-sm sm:px-4 sm:text-sm"
              value="tro-ly"
            >
              <Headphones aria-hidden="true" data-icon="inline-start" />
              <span>Trợ lý giọng nói</span>
            </TabsTrigger>
            <TabsTrigger
              className="h-12 rounded-[17px] px-2 text-[12px] text-[#77716b] data-active:bg-white data-active:text-[#1c1a17] data-active:shadow-sm sm:px-4 sm:text-sm"
              value="nha-phat-trien"
            >
              <Code2 aria-hidden="true" data-icon="inline-start" />
              <span className="hidden sm:inline">Dành cho nhà phát triển</span>
              <span className="sm:hidden">Lập trình</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent className="mt-0" value="sang-tao">
            <CreativePanel isPlaying={isPlaying} onToggle={togglePlayback} />
          </TabsContent>
          <TabsContent className="mt-0" value="tro-ly">
            <AgentPanel isPlaying={isPlaying} onToggle={togglePlayback} />
          </TabsContent>
          <TabsContent className="mt-0" value="nha-phat-trien">
            <DeveloperPanel isPlaying={isPlaying} onToggle={togglePlayback} />
          </TabsContent>
        </Tabs>
      </div>
    </section>
  )
}
