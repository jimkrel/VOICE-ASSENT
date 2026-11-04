export type VoiceProfile = {
  id: string
  name: string
  engine?: "omnivoice" | "kokoro"
  style: string
  locale: string
  gender: string
  language: string
  description: string
  sampleText: string
  categories: string[]
  source: string
  tone: "aqua" | "violet" | "coral" | "blue" | "green"
  previewUrl?: string
}

export type VoiceSettings = {
  engine: "omnivoice" | "kokoro"
  speed: number
  stability: number
  similarity: number
  style: number
  distance: string
  space: string
  language: string
  lufs: boolean
  denoise: boolean
  format: string
}

export const defaultVoiceSettings: VoiceSettings = {
  engine: "omnivoice",
  speed: 0.95,
  stability: 45,
  similarity: 75,
  style: 5,
  distance: "Vừa",
  space: "Phòng thu khô",
  language: "Tự động",
  lufs: true,
  denoise: false,
  format: "WAV · 24 kHz",
}

export type HistoryItem = {
  filename: string
  audioUrl: string
  createdAt: string
  sizeKb: number
}

export const voiceCatalog: VoiceProfile[] = [
  {
    id: "af_heart",
    name: "Heart (Kokoro)",
    engine: "kokoro",
    style: "ấm áp, chân thực bậc nhất",
    locale: "US",
    gender: "Nữ",
    language: "English (US)",
    description: "Giọng nữ Mỹ truyền cảm, độ tự nhiên và cảm xúc cao nhất",
    sampleText: "The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken seven-digit code.",
    categories: ["Kokoro 82M", "US English", "Nữ (Female)"],
    source: "Kokoro-82M",
    tone: "aqua",
    previewUrl: "/api/voices/af_heart/preview"
  },
  {
    id: "af_bella",
    name: "Bella (Kokoro)",
    engine: "kokoro",
    style: "tươi sáng, rõ nét",
    locale: "US",
    gender: "Nữ",
    language: "English (US)",
    description: "Giọng nữ Mỹ trẻ trung, rõ ràng và giàu năng lượng",
    sampleText: "Welcome to our studio. Everything you hear is generated in real time with neural speech synthesis.",
    categories: ["Kokoro 82M", "US English", "Nữ (Female)"],
    source: "Kokoro-82M",
    tone: "coral",
    previewUrl: "/api/voices/af_bella/preview"
  },
  {
    id: "af_nicole",
    name: "Nicole (Kokoro)",
    engine: "kokoro",
    style: "nhẹ nhàng, thì thầm",
    locale: "US",
    gender: "Nữ",
    language: "English (US)",
    description: "Giọng nữ Mỹ êm dịu, phù hợp audiobook và ASMR",
    sampleText: "Close your eyes, take a deep breath, and let the quiet surrounding take over.",
    categories: ["Kokoro 82M", "US English", "Nữ (Female)"],
    source: "Kokoro-82M",
    tone: "violet",
    previewUrl: "/api/voices/af_nicole/preview"
  },
  {
    id: "am_adam",
    name: "Adam (Kokoro)",
    engine: "kokoro",
    style: "trầm ấm, uy tín phát thanh",
    locale: "US",
    gender: "Nam",
    language: "English (US)",
    description: "Giọng nam Mỹ đĩnh đạc, ấm áp, chuẩn phim tài liệu và podcast",
    sampleText: "Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.",
    categories: ["Kokoro 82M", "US English", "Nam (Male)"],
    source: "Kokoro-82M",
    tone: "blue",
    previewUrl: "/api/voices/am_adam/preview"
  },
  {
    id: "am_michael",
    name: "Michael (Kokoro)",
    engine: "kokoro",
    style: "tự nhiên, đối thoại",
    locale: "US",
    gender: "Nam",
    language: "English (US)",
    description: "Giọng nam Mỹ đời thường, gần gũi và chân thật",
    sampleText: "I never thought technology would get this good, but hearing this voice changes everything.",
    categories: ["Kokoro 82M", "US English", "Nam (Male)"],
    source: "Kokoro-82M",
    tone: "blue",
    previewUrl: "/api/voices/am_michael/preview"
  },
  {
    id: "am_fenrir",
    name: "Fenrir (Kokoro)",
    engine: "kokoro",
    style: "điện ảnh, kịch tính",
    locale: "US",
    gender: "Nam",
    language: "English (US)",
    description: "Giọng nam Mỹ trầm nội lực, hợp trailer phim và cốt truyện ly kỳ",
    sampleText: "In the shadow of the mountains, an ancient secret was waiting to be unlocked.",
    categories: ["Kokoro 82M", "US English", "Nam (Male)"],
    source: "Kokoro-82M",
    tone: "coral",
    previewUrl: "/api/voices/am_fenrir/preview"
  },
  {
    id: "bf_emma",
    name: "Emma (Kokoro)",
    engine: "kokoro",
    style: "quý phái, chuẩn London",
    locale: "UK",
    gender: "Nữ",
    language: "English (UK)",
    description: "Giọng nữ Anh sang trọng, phát âm chuẩn Received Pronunciation",
    sampleText: "Good evening. It is an absolute pleasure to welcome you to tonight's performance.",
    categories: ["Kokoro 82M", "UK English", "Nữ (Female)"],
    source: "Kokoro-82M",
    tone: "violet",
    previewUrl: "/api/voices/bf_emma/preview"
  },
  {
    id: "bm_george",
    name: "George (Kokoro)",
    engine: "kokoro",
    style: "BBC, học thuật, uyên bác",
    locale: "UK",
    gender: "Nam",
    language: "English (UK)",
    description: "Giọng nam Anh trưởng thành, chuẩn đài phát thanh BBC",
    sampleText: "History reminds us that true progress often arrives not with a shout, but with a whisper.",
    categories: ["Kokoro 82M", "UK English", "Nam (Male)"],
    source: "Kokoro-82M",
    tone: "green",
    previewUrl: "/api/voices/bm_george/preview"
  },
  {
    id: "bm_lewis",
    name: "Lewis (Kokoro)",
    engine: "kokoro",
    style: "thân thiện, ấm áp",
    locale: "UK",
    gender: "Nam",
    language: "English (UK)",
    description: "Giọng nam Anh trẻ trung, nhịp điệu tự nhiên và cuốn hút",
    sampleText: "Have you ever wondered what lies beyond the edges of the known universe?",
    categories: ["Kokoro 82M", "UK English", "Nam (Male)"],
    source: "Kokoro-82M",
    tone: "blue",
    previewUrl: "/api/voices/bm_lewis/preview"
  },
  {
    "id": "hope",
    "name": "Hope",
    "style": "upbeat and clear",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "Trong trẻo, ngọt ngào, tươi sáng",
    "sampleText": "Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken seven-digit code.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "aqua",
    "previewUrl": "/api/voices/hope/preview"
  },
  {
    "id": "marcus",
    "name": "Marcus",
    "style": "documentary and crime",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "Trầm, rõ nét, phù hợp phim tài liệu",
    "sampleText": "The year was 1994. A signal appeared from a station no one had used in decades.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Hệ thống",
    "tone": "blue",
    "previewUrl": "/api/voices/marcus/preview"
  },
  {
    "id": "liam",
    "name": "Liam",
    "style": "storyteller and essay",
    "locale": "UK",
    "gender": "Nam",
    "language": "English (UK)",
    "description": "Ấm áp, gần gũi, nhịp kể tự nhiên",
    "sampleText": "Have you ever wondered why some stories stay with you forever?",
    "categories": [
      "UK English",
      "Nam (Male)"
    ],
    "source": "Hệ thống",
    "tone": "violet",
    "previewUrl": "/api/voices/liam/preview"
  },
  {
    "id": "alex",
    "name": "Alex",
    "style": "movie recap and shorts",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "Năng lượng, nhịp nhanh, hợp video ngắn",
    "sampleText": "In a city that never sleeps, one message changed everything.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Hệ thống",
    "tone": "coral",
    "previewUrl": "/api/voices/alex/preview"
  },
  {
    "id": "minh-anh",
    "name": "Minh Anh",
    "style": "ấm áp và rõ ràng",
    "locale": "Việt Nam",
    "gender": "Nữ",
    "language": "Tiếng Việt",
    "description": "Giọng nữ miền Bắc, nhẹ nhàng và tự nhiên",
    "sampleText": "Xin chào, mời bạn cùng khám phá câu chuyện hôm nay.",
    "categories": [
      "Tiếng Việt",
      "Nữ (Female)"
    ],
    "source": "Hệ thống",
    "tone": "green",
    "previewUrl": "/api/voices/minh-anh/preview"
  },
  {
    "id": "bao-ngoc",
    "name": "Bảo Ngọc",
    "style": "trẻ trung và tươi sáng",
    "locale": "Việt Nam",
    "gender": "Nữ",
    "language": "Tiếng Việt",
    "description": "Phát âm rõ, giàu cảm xúc, hợp nội dung thương hiệu",
    "sampleText": "Bắt đầu một ngày mới với cảm hứng và những ý tưởng thật khác biệt.",
    "categories": [
      "Tiếng Việt",
      "Nữ (Female)"
    ],
    "source": "Giọng tự tạo",
    "tone": "coral",
    "previewUrl": "/api/voices/bao-ngoc/preview"
  },
  {
    "id": "gia-huy",
    "name": "Gia Huy",
    "style": "nam ấm áp, truyền cảm",
    "locale": "Việt Nam",
    "gender": "Nam",
    "language": "Tiếng Việt",
    "description": "Giọng nam tự sự, thuyết minh và review",
    "sampleText": "Xin chào, đây là giọng đọc nam truyền cảm chuẩn phòng thu studio.",
    "categories": [
      "Tiếng Việt",
      "Nam (Male)"
    ],
    "source": "Hệ thống",
    "tone": "blue",
    "previewUrl": "/api/voices/gia-huy/preview"
  },
  {
    "id": "roger",
    "name": "Roger",
    "style": "podcast & conversational",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Tự nhiên, phóng khoáng, phong độ • Podcast, Vlogs",
    "sampleText": "It is not so important to know everything as to appreciate what we learn.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "aqua",
    "previewUrl": "/api/voices/roger/preview"
  },
  {
    "id": "sarah",
    "name": "Sarah",
    "style": "news & television",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "US Nữ • Chững chạc, điềm tĩnh, chuyên nghiệp • Bản tin, TV, Đánh giá",
    "sampleText": "The years teach much which the days never know.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "blue",
    "previewUrl": "/api/voices/sarah/preview"
  },
  {
    "id": "laura",
    "name": "Laura",
    "style": "pop culture & reaction",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "US Nữ • Cá tính, sắc sảo, năng động • Reaction, Pop Culture",
    "sampleText": "Our distrust is very expensive.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "violet",
    "previewUrl": "/api/voices/laura/preview"
  },
  {
    "id": "george",
    "name": "George",
    "style": "british storyteller",
    "locale": "UK",
    "gender": "Nam",
    "language": "English (UK)",
    "description": "UK Nam • Trầm ấm, quý phái, lôi cuốn • Kể chuyện, Phim tài liệu",
    "sampleText": "God has given you one face and you make yourself another.",
    "categories": [
      "UK English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "coral",
    "previewUrl": "/api/voices/george/preview"
  },
  {
    "id": "callum",
    "name": "Callum",
    "style": "character & animation",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Giọng khàn nhân vật, kịch tính • Hoạt hình, Phim",
    "sampleText": "Life without love is like a tree without blossoms or fruit.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "green",
    "previewUrl": "/api/voices/callum/preview"
  },
  {
    "id": "alice",
    "name": "Alice",
    "style": "science & academic",
    "locale": "UK",
    "gender": "Nữ",
    "language": "English (UK)",
    "description": "UK Nữ • Chuẩn giọng Anh học thuật, sư phạm • Khoa học, E-learning",
    "sampleText": "Just trust yourself, then you will know how to live.",
    "categories": [
      "UK English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "aqua",
    "previewUrl": "/api/voices/alice/preview"
  },
  {
    "id": "matilda",
    "name": "Matilda",
    "style": "explainer & how-to",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "US Nữ • Tươi sáng, rành mạch, dễ hiểu • Hướng dẫn, Đời sống",
    "sampleText": "Ideas are the beginning points of all fortunes.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "blue",
    "previewUrl": "/api/voices/matilda/preview"
  },
  {
    "id": "will",
    "name": "Will",
    "style": "chill & gaming",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Thư thái, gần gũi, trẻ trung • Gaming, Chill Story",
    "sampleText": "We make our own fortunes and we call them fate.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "violet",
    "previewUrl": "/api/voices/will/preview"
  },
  {
    "id": "jessica",
    "name": "Jessica",
    "style": "vlog & lifestyle",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "US Nữ • Trẻ trung, ngọt ngào, tươi vui • Lifestyle, Vlogs, Shorts",
    "sampleText": "If you spend your whole life waiting for the storm, you'll never enjoy the sunshine.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "coral",
    "previewUrl": "/api/voices/jessica/preview"
  },
  {
    "id": "eric",
    "name": "Eric",
    "style": "corporate & review",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Lịch lãm, đáng tin cậy • Tài chính, Doanh nghiệp",
    "sampleText": "Gratitude is riches, complained is poverty.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "green",
    "previewUrl": "/api/voices/eric/preview"
  },
  {
    "id": "bella",
    "name": "Bella",
    "style": "audiobook & narration",
    "locale": "US",
    "gender": "Nữ",
    "language": "English (US)",
    "description": "US Nữ • Dịu dàng, chuẩn phát thanh • Đọc truyện, Sách nói",
    "sampleText": "In the theater of life, we are all actors sharing the same scene.",
    "categories": [
      "US English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "aqua",
    "previewUrl": "/api/voices/bella/preview"
  },
  {
    "id": "brian",
    "name": "Brian",
    "style": "documentary & essay",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Trầm ấm, truyền cảm sâu lắng • Video Essay, Phim tài liệu",
    "sampleText": "The thing always happens that you really believe in, and the belief in a thing makes it happen.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "blue",
    "previewUrl": "/api/voices/brian/preview"
  },
  {
    "id": "daniel",
    "name": "Daniel",
    "style": "formal news anchor",
    "locale": "UK",
    "gender": "Nam",
    "language": "English (UK)",
    "description": "UK Nam • Chuẩn đài BBC, trang trọng, quyền uy • Thời sự, Phân tích",
    "sampleText": "The world is round, and the place which may seem like the end may also be the beginning.",
    "categories": [
      "UK English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "violet",
    "previewUrl": "/api/voices/daniel/preview"
  },
  {
    "id": "lily",
    "name": "Lily",
    "style": "drama & literature",
    "locale": "UK",
    "gender": "Nữ",
    "language": "English (UK)",
    "description": "UK Nữ • Nhung mượt diễn xuất, giàu cảm xúc • Kịch nghệ, Văn học",
    "sampleText": "I have never been hurt by anything I didn't say.",
    "categories": [
      "UK English",
      "Nữ (Female)"
    ],
    "source": "Mẫu Studio",
    "tone": "coral",
    "previewUrl": "/api/voices/lily/preview"
  },
  {
    "id": "adam",
    "name": "Adam",
    "style": "shorts & hook",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Đanh thép, quyền lực, nhịp dồn dập • Shorts, Tech Review",
    "sampleText": "Our distrust is very expensive.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "green",
    "previewUrl": "/api/voices/adam/preview"
  },
  {
    "id": "bill",
    "name": "Bill",
    "style": "old sage & history",
    "locale": "US",
    "gender": "Nam",
    "language": "English (US)",
    "description": "US Nam • Lão thành thông thái, uyên bác • Lịch sử, Sách kinh điển",
    "sampleText": "As we are liberated from our own fear, our presence automatically liberates others.",
    "categories": [
      "US English",
      "Nam (Male)"
    ],
    "source": "Mẫu Studio",
    "tone": "aqua",
    "previewUrl": "/api/voices/bill/preview"
  }
]

export function getVoiceById(id: string, list: VoiceProfile[] = voiceCatalog) {
  return list.find((voice) => voice.id === id) ?? list[0] ?? voiceCatalog[0]
}
