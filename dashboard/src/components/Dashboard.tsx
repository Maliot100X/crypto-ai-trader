'use client'

import { useState, useEffect } from 'react'

interface StatusData {
  agents?: { total_agents: number; active_agents: number }
  strategies?: Array<{ name: string; type: string; enabled: boolean }>
  positions?: { open_positions: number; total_realized_pnl: number; win_rate: number }
  wallets?: { total_wallets: number; active_wallet: string | null }
}

interface BacktestResult {
  roi_pct: number
  sharpe_ratio: number
  max_drawdown_pct: number
  win_rate: number
  total_trades: number
  strategy: string
}

function StatCard({ title, value, subtitle, color = 'sol-green' }: {
  title: string; value: string | number; subtitle?: string; color?: string
}) {
  return (
    <div className="glass-card">
      <p className="text-sm text-gray-400 mb-1">{title}</p>
      <p className={`stat-value text-${color}`}>{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  )
}

export default function Dashboard() {
  const [status, setStatus] = useState<StatusData | null>(null)
  const [backtest, setBacktest] = useState<BacktestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'overview' | 'agents' | 'trading' | 'backtest'>('overview')

  // Simulated data for demo mode (when API is not available)
  useEffect(() => {
    setStatus({
      agents: { total_agents: 5, active_agents: 3 },
      strategies: [
        { name: 'momentum_breakout', type: 'momentum', enabled: true },
        { name: 'mean_reversion', type: 'mean_reversion', enabled: true },
        { name: 'ai_signal', type: 'ai_signal', enabled: true },
        { name: 'sentiment_trade', type: 'sentiment', enabled: false },
        { name: 'cross_exchange_arb', type: 'arbitrage', enabled: false },
      ],
      positions: { open_positions: 2, total_realized_pnl: 1247.50, win_rate: 0.67 },
      wallets: { total_wallets: 1, active_wallet: 'Bx7k...m2Fp' },
    })
  }, [])

  const runBacktest = () => {
    setLoading(true)
    setTimeout(() => {
      setBacktest({
        roi_pct: 23.47,
        sharpe_ratio: 1.42,
        max_drawdown_pct: 8.3,
        win_rate: 62.5,
        total_trades: 48,
        strategy: 'momentum',
      })
      setLoading(false)
    }, 1500)
  }

  const tabs = [
    { key: 'overview' as const, label: 'Overview' },
    { key: 'agents' as const, label: 'Agents' },
    { key: 'trading' as const, label: 'Trading' },
    { key: 'backtest' as const, label: 'Backtest' },
  ]

  return (
    <div className="relative z-10 p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold gradient-text">Solana Agent Trader</h1>
          <p className="text-gray-400 mt-1">Self-Assembling AI Trading Lab</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center">
            <span className="status-dot active"></span>
            <span className="text-sm text-sol-green">System Online</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab.key
                ? 'bg-sol-purple/20 text-sol-purple border border-sol-purple/30'
                : 'bg-dark-card text-gray-400 hover:text-white border border-dark-border'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatCard title="Active Agents" value={status?.agents?.active_agents || 0} subtitle={`of ${status?.agents?.total_agents || 0} total`} />
            <StatCard title="Open Positions" value={status?.positions?.open_positions || 0} color="sol-blue" />
            <StatCard title="Total P&L" value={`$${status?.positions?.total_realized_pnl?.toFixed(2) || '0.00'}`} color="sol-green" />
            <StatCard title="Win Rate" value={`${((status?.positions?.win_rate || 0) * 100).toFixed(0)}%`} color="sol-purple" />
          </div>

          {/* Strategies */}
          <div className="glass-card mb-6">
            <h2 className="text-lg font-semibold text-white mb-4">Active Strategies</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {status?.strategies?.map((s) => (
                <div key={s.name} className="flex items-center justify-between bg-dark/50 rounded-lg p-3">
                  <div>
                    <p className="text-white text-sm font-medium">{s.name.replace(/_/g, ' ')}</p>
                    <p className="text-gray-500 text-xs">{s.type}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs ${s.enabled ? 'bg-sol-green/20 text-sol-green' : 'bg-gray-700 text-gray-400'}`}>
                    {s.enabled ? 'Active' : 'Disabled'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Wallet */}
          <div className="glass-card">
            <h2 className="text-lg font-semibold text-white mb-3">Wallet</h2>
            <div className="flex items-center gap-3">
              <span className="status-dot active"></span>
              <code className="text-sol-blue text-sm">{status?.wallets?.active_wallet || 'No wallet connected'}</code>
              <span className="text-gray-500 text-xs">({status?.wallets?.total_wallets || 0} wallets)</span>
            </div>
          </div>
        </>
      )}

      {/* Agents Tab */}
      {activeTab === 'agents' && (
        <div className="glass-card">
          <h2 className="text-lg font-semibold text-white mb-4">Agent Fleet</h2>
          <div className="space-y-3">
            {['Agent Alpha', 'Agent Beta', 'Agent Gamma', 'Agent Delta', 'Agent Omega'].map((name, i) => (
              <div key={name} className="flex items-center justify-between bg-dark/50 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <span className={`status-dot ${i < 3 ? 'active' : 'inactive'}`}></span>
                  <div>
                    <p className="text-white font-medium">{name}</p>
                    <p className="text-gray-500 text-xs">{['aggressive', 'conservative', 'analytical', 'momentum', 'contrarian'][i]} personality</p>
                  </div>
                </div>
                <span className={`text-sm ${i < 3 ? 'text-sol-green' : 'text-gray-500'}`}>
                  {i < 3 ? 'Running' : 'Idle'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Trading Tab */}
      {activeTab === 'trading' && (
        <div className="space-y-4">
          <div className="glass-card">
            <h2 className="text-lg font-semibold text-white mb-4">Market Data</h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-dark/50 rounded-lg p-3 text-center">
                <p className="text-gray-400 text-xs">SOL/USD</p>
                <p className="text-2xl font-bold text-white">$148.72</p>
                <p className="text-sol-green text-sm">+2.34%</p>
              </div>
              <div className="bg-dark/50 rounded-lg p-3 text-center">
                <p className="text-gray-400 text-xs">BTC/USD</p>
                <p className="text-2xl font-bold text-white">$64,820</p>
                <p className="text-sol-green text-sm">+1.12%</p>
              </div>
              <div className="bg-dark/50 rounded-lg p-3 text-center">
                <p className="text-gray-400 text-xs">ETH/USD</p>
                <p className="text-2xl font-bold text-white">$3,456</p>
                <p className="text-red-400 text-sm">-0.45%</p>
              </div>
            </div>
          </div>
          <div className="glass-card">
            <h2 className="text-lg font-semibold text-white mb-4">Recent Signals</h2>
            <div className="space-y-2">
              {[
                { type: 'RSI Oversold', action: 'BUY', symbol: 'SOL/USD', strength: 'Strong' },
                { type: 'MACD Bullish', action: 'BUY', symbol: 'SOL/USD', strength: 'Medium' },
                { type: 'BB Upper Touch', action: 'SELL', symbol: 'BTC/USD', strength: 'Medium' },
              ].map((sig, i) => (
                <div key={i} className="flex items-center justify-between bg-dark/50 rounded-lg p-3">
                  <div>
                    <p className="text-white text-sm">{sig.type}</p>
                    <p className="text-gray-500 text-xs">{sig.symbol}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400">{sig.strength}</span>
                    <span className={`px-2 py-1 rounded text-xs font-bold ${sig.action === 'BUY' ? 'bg-sol-green/20 text-sol-green' : 'bg-red-500/20 text-red-400'}`}>
                      {sig.action}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Backtest Tab */}
      {activeTab === 'backtest' && (
        <div className="space-y-4">
          <div className="glass-card">
            <h2 className="text-lg font-semibold text-white mb-4">Run Backtest</h2>
            <div className="flex gap-3">
              <button
                onClick={runBacktest}
                disabled={loading}
                className="px-6 py-3 bg-sol-purple/20 border border-sol-purple/30 text-sol-purple rounded-lg hover:bg-sol-purple/30 transition-all disabled:opacity-50"
              >
                {loading ? 'Running...' : 'Run Momentum Backtest'}
              </button>
            </div>
          </div>

          {backtest && (
            <div className="glass-card">
              <h2 className="text-lg font-semibold text-white mb-4">Backtest Results: {backtest.strategy}</h2>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <p className="text-gray-400 text-xs">ROI</p>
                  <p className={`text-2xl font-bold ${backtest.roi_pct > 0 ? 'text-sol-green' : 'text-red-400'}`}>
                    {backtest.roi_pct}%
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 text-xs">Sharpe Ratio</p>
                  <p className="text-2xl font-bold text-sol-blue">{backtest.sharpe_ratio}</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 text-xs">Max Drawdown</p>
                  <p className="text-2xl font-bold text-red-400">{backtest.max_drawdown_pct}%</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 text-xs">Win Rate</p>
                  <p className="text-2xl font-bold text-sol-purple">{backtest.win_rate}%</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 text-xs">Total Trades</p>
                  <p className="text-2xl font-bold text-white">{backtest.total_trades}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
