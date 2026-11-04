import { Analytics } from '@vercel/analytics/next'
import { Be_Vietnam_Pro } from 'next/font/google'
import { ThemeProvider } from 'next-themes'
import type { Metadata, Viewport } from 'next'
import { VoiceStudioProvider } from '@/components/voice-studio-context'
import { StudioShell } from '@/components/studio-shell'
import './globals.css'

const beVietnamPro = Be_Vietnam_Pro({
  weight: ['400', '500', '600', '700'],
  subsets: ['latin', 'vietnamese'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Thành Âm — Không gian sáng tạo giọng nói',
  description:
    'Đọc kịch bản, tạo giọng mới, đổi giọng và khám phá thư viện giọng đọc tiếng Việt, tiếng Anh trong một không gian sáng tạo âm thanh.',
  applicationName: 'Thành Âm',
  openGraph: {
    type: 'website',
    locale: 'vi_VN',
    siteName: 'Thành Âm',
    title: 'Thành Âm — Giọng nói tiếng Việt tự nhiên',
    description:
      'Đọc kịch bản, tạo giọng mới, đổi giọng và khám phá thư viện giọng đọc trong không gian sáng tạo âm thanh Thành Âm.'
  },
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export const viewport: Viewport = {
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#f8f7f5' },
    { media: '(prefers-color-scheme: dark)', color: '#1e1b26' },
  ],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <body className={`${beVietnamPro.className} antialiased`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <VoiceStudioProvider>
            <StudioShell>{children}</StudioShell>
          </VoiceStudioProvider>
          {process.env.NODE_ENV === 'production' && <Analytics />}
        </ThemeProvider>
      </body>
    </html>
  )
}
