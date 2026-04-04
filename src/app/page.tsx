'use client'

import dynamic from 'next/dynamic'
import Dashboard from '@/components/Dashboard'

// Dynamic import for Three.js (SSR disabled)
const Scene3D = dynamic(() => import('@/components/Scene3D'), { ssr: false })

export default function Home() {
  return (
    <main className="min-h-screen relative">
      {/* 3D Animated Background */}
      <Scene3D fullScreen />

      {/* Dashboard Overlay */}
      <Dashboard />

      {/* Footer */}
      <footer className="relative z-10 text-center py-8 text-gray-600 text-sm">
        <p className="gradient-text font-semibold">Solana Agent Trader v1.0</p>
        <p className="mt-1">Self-Assembling AI Trading Lab</p>
      </footer>
    </main>
  )
}
