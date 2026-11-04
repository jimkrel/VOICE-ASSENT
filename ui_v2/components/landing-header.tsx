"use client"

import { useState } from "react"
import { ArrowUpRight, AudioLines, Menu, X } from "lucide-react"
import { Button, buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const navigationItems = [
  { label: "Sản phẩm", href: "#san-pham" },
  { label: "Ứng dụng", href: "#ung-dung" },
  { label: "Công nghệ", href: "#cong-nghe" },
]

export function LandingHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <>
      <div className="border-b border-[#e9e4dd] bg-[#f3f0eb]">
        <div className="mx-auto flex min-h-10 max-w-[1280px] items-center justify-center gap-3 px-4 text-center text-xs text-[#5d5852] sm:text-sm">
          <span className="rounded-full border border-[#d4ccc1] px-2 py-0.5 text-[9px] font-semibold tracking-[0.14em] text-[#7b604b] sm:text-[10px]">
            MỚI
          </span>
          <p className="whitespace-nowrap">Giọng nói tiếng Việt, tự nhiên hơn.</p>
          <a
            className="hidden items-center gap-1 font-medium text-[#211f1c] underline-offset-4 hover:underline sm:inline-flex"
            href="#cong-nghe"
          >
            Khám phá <ArrowUpRight aria-hidden="true" className="size-3.5" />
          </a>
        </div>
      </div>

      <header className="sticky top-0 z-40 border-b border-black/[0.06] bg-[#fbfaf8]/90 backdrop-blur-xl">
        <div className="relative mx-auto flex h-[74px] max-w-[1280px] items-center justify-between px-5 sm:px-8 lg:px-10">
          <a
            aria-label="Thành Âm, về đầu trang"
            className="inline-flex items-center gap-2.5"
            href="#trang-chu"
            onClick={() => setMobileMenuOpen(false)}
          >
            <span className="grid size-9 place-items-center rounded-full bg-[#e9ded2] text-[#654b38]">
              <AudioLines aria-hidden="true" className="size-[18px]" />
            </span>
            <span className="text-[19px] font-semibold tracking-[-0.07em] text-[#191816]">
              thành âm
            </span>
          </a>

          <nav
            aria-label="Điều hướng chính"
            className="hidden items-center gap-8 md:flex"
          >
            {navigationItems.map((item) => (
              <a
                className="text-sm text-[#615d57] transition-colors hover:text-[#171614]"
                href={item.href}
                key={item.href}
              >
                {item.label}
              </a>
            ))}
          </nav>

          <div className="hidden items-center gap-3 md:flex">
            <a
              className={cn(
                buttonVariants({ variant: "ghost", size: "lg" }),
                "h-10 rounded-full px-4 text-sm",
              )}
              href="#demo"
            >
              Xem bản thử
            </a>
            <a
              className={cn(
                buttonVariants({ size: "lg" }),
                "h-10 rounded-full px-5 text-sm",
              )}
              href="#demo"
            >
              Bắt đầu miễn phí
              <ArrowUpRight aria-hidden="true" data-icon="inline-end" />
            </a>
          </div>

          <Button
            aria-controls="menu-di-dong"
            aria-expanded={mobileMenuOpen}
            aria-label={mobileMenuOpen ? "Đóng điều hướng" : "Mở điều hướng"}
            className="size-10 rounded-full bg-white md:hidden"
            onClick={() => setMobileMenuOpen((isOpen) => !isOpen)}
            size="icon"
            type="button"
            variant="outline"
          >
            {mobileMenuOpen ? (
              <X aria-hidden="true" />
            ) : (
              <Menu aria-hidden="true" />
            )}
          </Button>

          {mobileMenuOpen && (
            <nav
              aria-label="Điều hướng di động"
              className="absolute inset-x-4 top-[calc(100%-1px)] grid gap-1 rounded-b-[24px] border border-t-0 border-[#e8e4de] bg-[#fbfaf8] p-3 shadow-[0_18px_45px_rgba(35,30,25,0.12)] md:hidden"
              id="menu-di-dong"
            >
              {navigationItems.map((item) => (
                <a
                  className="rounded-xl px-4 py-3 text-sm text-[#46413b] transition-colors hover:bg-[#f0ede8]"
                  href={item.href}
                  key={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.label}
                </a>
              ))}
              <a
                className={cn(
                  buttonVariants({ size: "lg" }),
                  "mt-2 h-11 justify-center rounded-full",
                )}
                href="#demo"
                onClick={() => setMobileMenuOpen(false)}
              >
                Bắt đầu miễn phí
                <ArrowUpRight aria-hidden="true" data-icon="inline-end" />
              </a>
            </nav>
          )}
        </div>
      </header>
    </>
  )
}
