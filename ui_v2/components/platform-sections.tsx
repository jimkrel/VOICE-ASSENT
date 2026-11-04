import {
  ArrowUpRight,
  AudioLines,
  BookOpenText,
  Headphones,
  Languages,
  MessageCircle,
  Mic2,
  Sparkles,
} from "lucide-react"

const productCards = [
  {
    index: "01",
    title: "Tạo giọng nói",
    description:
      "Biến văn bản thành lời kể giàu sắc thái cho video, sách nói và nội dung số.",
    icon: <AudioLines aria-hidden="true" className="size-5" />,
    style: "bg-[#211f1b] text-white",
    iconStyle: "bg-white/10 text-[#efc7a5]",
    copyStyle: "text-white/65",
    indexStyle: "text-white/45",
    arrowStyle: "text-white/65",
  },
  {
    index: "02",
    title: "Lồng tiếng tự nhiên",
    description:
      "Đưa nội dung đến gần hơn với khán giả bằng bản lồng tiếng mượt mà, nhất quán.",
    icon: <Languages aria-hidden="true" className="size-5" />,
    style: "bg-white text-[#211f1b]",
    iconStyle: "bg-[#f0e8df] text-[#8b6548]",
    copyStyle: "text-[#777067]",
    indexStyle: "text-[#a49b91]",
    arrowStyle: "text-[#8f6c51]",
  },
  {
    index: "03",
    title: "Trợ lý giọng nói",
    description:
      "Tạo những cuộc hội thoại hữu ích cho chăm sóc khách hàng và dịch vụ của bạn.",
    icon: <Headphones aria-hidden="true" className="size-5" />,
    style: "bg-[#e9e6e0] text-[#211f1b]",
    iconStyle: "bg-white/75 text-[#68705c]",
    copyStyle: "text-[#6e6962]",
    indexStyle: "text-[#a49b91]",
    arrowStyle: "text-[#788065]",
  },
]

const useCases = [
  {
    title: "Sáng tạo nội dung",
    description: "Video, podcast, sách nói và nội dung mạng xã hội.",
    icon: <Mic2 aria-hidden="true" className="size-5" />,
  },
  {
    title: "Dịch vụ khách hàng",
    description: "Trợ lý luôn sẵn sàng trong những cuộc hội thoại thường ngày.",
    icon: <MessageCircle aria-hidden="true" className="size-5" />,
  },
  {
    title: "Học tập và đào tạo",
    description: "Bài học, hướng dẫn và trải nghiệm học tập dễ tiếp cận hơn.",
    icon: <BookOpenText aria-hidden="true" className="size-5" />,
  },
]

export function PlatformSections() {
  return (
    <>
      <section
        className="bg-[#f0eeea] px-5 py-20 sm:px-8 sm:py-24 lg:px-10 lg:py-28"
        id="san-pham"
      >
        <div className="mx-auto max-w-[1280px]">
          <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end">
            <div>
              <p className="text-[10px] font-semibold tracking-[0.16em] text-[#9a765b] sm:text-[11px]">
                MỘT NỀN TẢNG · NHIỀU CÁCH KỂ
              </p>
              <h2 className="mt-3 max-w-[710px] text-4xl font-medium leading-[1.05] tracking-[-0.065em] text-[#1c1a17] sm:text-5xl lg:text-[3.8rem]">
                Âm thanh hay mở ra nhiều khả năng.
              </h2>
            </div>
            <p className="max-w-[390px] text-sm leading-6 text-[#716b63] sm:text-[15px]">
              Tạo nên trải nghiệm bằng giọng nói phù hợp với câu chuyện, thương
              hiệu và người nghe của bạn.
            </p>
          </div>

          <div className="mt-10 grid gap-3 md:grid-cols-3">
            {productCards.map((card) => (
              <a
                className={`group flex min-h-[286px] flex-col rounded-[26px] p-6 transition-transform duration-300 hover:-translate-y-1 sm:p-7 ${card.style}`}
                href="#demo"
                key={card.index}
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`grid size-11 place-items-center rounded-full ${card.iconStyle}`}
                  >
                    {card.icon}
                  </span>
                  <span className={`text-xs font-medium ${card.indexStyle}`}>
                    {card.index}
                  </span>
                </div>
                <div className="mt-auto pt-12">
                  <h3 className="text-xl font-medium tracking-[-0.04em] sm:text-2xl">
                    {card.title}
                  </h3>
                  <p className={`mt-2 max-w-[330px] text-sm leading-6 ${card.copyStyle}`}>
                    {card.description}
                  </p>
                  <span className="mt-5 inline-flex items-center gap-2 text-xs font-medium">
                    Khám phá
                    <ArrowUpRight
                      aria-hidden="true"
                      className={`size-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 ${card.arrowStyle}`}
                    />
                  </span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      <section
        className="px-5 py-20 sm:px-8 sm:py-24 lg:px-10 lg:py-28"
        id="ung-dung"
      >
        <div className="mx-auto max-w-[1280px]">
          <div className="flex flex-col gap-4">
            <p className="text-[10px] font-semibold tracking-[0.16em] text-[#9a765b] sm:text-[11px]">
              ĐƯỢC TẠO CHO NHỮNG ĐIỀU BẠN ĐANG LÀM
            </p>
            <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
              <h2 className="max-w-[720px] text-4xl font-medium leading-[1.06] tracking-[-0.065em] text-[#1c1a17] sm:text-5xl lg:text-[3.7rem]">
                Một giọng nói phù hợp cho mọi bối cảnh.
              </h2>
              <p className="max-w-[350px] text-sm leading-6 text-[#716b63] sm:text-[15px]">
                Từ nội dung được kể lại đến dịch vụ luôn sẵn sàng lắng nghe.
              </p>
            </div>
          </div>

          <div className="mt-10 grid gap-3 md:grid-cols-3">
            {useCases.map((item, index) => (
              <article
                className="rounded-[24px] border border-[#e8e4de] bg-white p-6 sm:p-7"
                key={item.title}
              >
                <div className="flex items-center justify-between">
                  <span className="grid size-10 place-items-center rounded-full bg-[#f0ece6] text-[#85674d]">
                    {item.icon}
                  </span>
                  <span className="text-[10px] font-medium tracking-[0.12em] text-[#aaa197]">
                    0{index + 1}
                  </span>
                </div>
                <h3 className="mt-9 text-lg font-medium tracking-[-0.035em] text-[#26231f]">
                  {item.title}
                </h3>
                <p className="mt-2 max-w-[300px] text-sm leading-6 text-[#777067]">
                  {item.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="px-5 pb-20 sm:px-8 sm:pb-24 lg:px-10 lg:pb-28" id="cong-nghe">
        <div className="relative mx-auto max-w-[1280px] overflow-hidden rounded-[30px] bg-[#211f1b] px-6 py-10 text-white sm:px-10 sm:py-12 lg:px-14 lg:py-16">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-20 -top-32 size-[330px] rounded-full bg-[radial-gradient(circle_at_35%_40%,rgba(232,172,126,0.26),rgba(232,172,126,0)_68%)]"
          />
          <div className="relative grid gap-10 lg:grid-cols-[1fr_0.8fr] lg:items-end lg:gap-16">
            <div>
              <p className="inline-flex items-center gap-2 text-[10px] font-semibold tracking-[0.16em] text-[#e6bd9e] sm:text-[11px]">
                <Sparkles aria-hidden="true" className="size-3.5" />
                TIẾNG VIỆT, VỚI SẮC THÁI RIÊNG
              </p>
              <h2 className="mt-4 max-w-[700px] text-4xl font-medium leading-[1.04] tracking-[-0.065em] sm:text-5xl lg:text-[3.7rem]">
                Để mỗi câu chuyện được kể đúng cách.
              </h2>
              <p className="mt-4 max-w-[540px] text-sm leading-6 text-white/65 sm:text-[15px]">
                Một trải nghiệm tập trung vào ngôn ngữ, nhịp điệu và cảm xúc của
                người nghe Việt Nam.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
              {[
                "Ngữ điệu gần gũi, dễ nghe",
                "Chất giọng linh hoạt theo nội dung",
                "Sẵn sàng mở rộng cùng sản phẩm",
              ].map((benefit) => (
                <div
                  className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3.5 text-sm text-white/80"
                  key={benefit}
                >
                  <span className="size-1.5 rounded-full bg-[#e4b690]" />
                  {benefit}
                </div>
              ))}
              <a
                className="mt-1 inline-flex items-center gap-2 px-1 py-2 text-sm font-medium text-[#f1d4bc] transition-colors hover:text-white"
                href="#demo"
              >
                Khám phá bản trải nghiệm
                <ArrowUpRight aria-hidden="true" className="size-4" />
              </a>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
