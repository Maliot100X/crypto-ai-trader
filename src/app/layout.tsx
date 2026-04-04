import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Solana Agent Trader - AI Trading Lab',
  description: 'Self-assembling autonomous AI trading platform with 3D visualization',
  icons: { icon: '/favicon.ico' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-dark">
        {children}
      </body>
    </html>
  )
}
