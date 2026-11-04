import { ArrowUpRight, AudioLines } from "lucide-react"

const footerLinks = [
  { label: "Sản phẩm", href: "#san-pham" },
  { label: "Ứng dụng", href: "#ung-dung" },
  { label: "Công nghệ", href: "#cong-nghe" },
]

export function SiteFooter() {
  return (
    <footer className="border-t border-[#e9e4de] bg-[#f3f1ed] px-5 pb-7 pt-10 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-[1280px]">
        <div className="flex flex-col justify-between gap-8 pb-10 md:flex-row md:items-start">
          <div className="max-w-[390px]">
            <a
              aria-label="Thành Âm, về đầu trang"
              className="inline-flex items-center gap-2.5"
              href="#trang-chu"
            >
              <span className="grid size-9 place-items-center rounded-full bg-[#e6ddd3] text-[#654b38]">
                <AudioLines aria-hidden="true" className="size-[18px]" />
              </span>
              <span className="text-[19px] font-semibold tracking-[-0.07em] text-[#191816]">
                thành âm
              </span>
            </a>
            <p className="mt-4 text-sm leading-6 text-[#756f67]">
              Trao cho ý tưởng một giọng nói riêng — tự nhiên, gần gũi và giàu
              cảm xúc.
            </p>
          </div>

          <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:gap-12">
            <nav aria-label="Liên kết chân trang" className="flex gap-5 sm:gap-7">
              {footerLinks.map((link) => (
                <a
                  className="text-sm text-[#625d56] transition-colors hover:text-[#191816]"
                  href={link.href}
                  key={link.href}
                >
                  {link.label}
                </a>
              ))}
            </nav>
            <a
              className="inline-flex items-center gap-2 text-sm font-medium text-[#2b2824] transition-colors hover:text-[#8d6b53]"
              href="#demo"
            >
              Trải nghiệm ngay
              <ArrowUpRight aria-hidden="true" className="size-4" />
            </a>
          </div>
        </div>

        <div className="flex flex-col gap-2 border-t border-[#e4dfd9] pt-5 text-xs text-[#91897f] sm:flex-row sm:items-center sm:justify-between">
          <span>© 2026 Thành Âm. Thiết kế cho trải nghiệm bằng tiếng Việt.</span>
          <span>Giao diện minh họa · Chưa kết nối dịch vụ âm thanh.</span>
        </div>
      </div>
    </footer>
  )
}
