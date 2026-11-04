import { ArrowUpRight } from "lucide-react"
import { buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export function HeroSection() {
  return (
    <section
      className="px-5 pb-10 pt-16 sm:px-8 sm:pb-12 sm:pt-20 lg:px-10 lg:pb-14 lg:pt-[88px]"
      id="trang-chu"
    >
      <div className="mx-auto grid max-w-[1280px] gap-8 lg:grid-cols-[1.08fr_0.92fr] lg:items-end lg:gap-14">
        <div>
          <p className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#e8e2db] bg-white/70 px-3.5 py-2 text-[10px] font-semibold tracking-[0.16em] text-[#76675a] sm:text-[11px]">
            <span className="size-1.5 rounded-full bg-[#c27b54]" />
            NỀN TẢNG GIỌNG NÓI THÔNG MINH
          </p>
          <h1 className="max-w-[760px] text-[clamp(3.2rem,5.9vw,5.8rem)] font-normal leading-[1.01] tracking-[-0.075em] text-[#171614]">
            Đưa ý tưởng
            <span className="block text-[#8d6b53]">cất lên thành lời.</span>
          </h1>
        </div>

        <div className="flex flex-col gap-7 pb-1 lg:pb-2">
          <p className="max-w-[470px] text-base leading-7 text-[#625d56] sm:text-lg sm:leading-[1.7]">
            Tạo giọng nói tự nhiên, lồng tiếng video và xây trợ lý AI — trên một
            nền tảng được thiết kế cho tiếng Việt.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <a
              className={cn(
                buttonVariants({ size: "lg" }),
                "h-11 rounded-full px-5 text-sm",
              )}
              href="#demo"
            >
              Bắt đầu sáng tạo
              <ArrowUpRight aria-hidden="true" data-icon="inline-end" />
            </a>
            <a
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "h-11 rounded-full border-[#e4dfd8] bg-white/70 px-5 text-sm",
              )}
              href="#san-pham"
            >
              Khám phá nền tảng
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
