const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'

export async function fetchAPI(endpoint: string, options?: RequestInit) {
  try {
    const res = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options?.headers },
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return await res.json()
  } catch (error) {
    console.error(`API fetch error for ${endpoint}:`, error)
    return null
  }
}

export const api = {
  getStatus: () => fetchAPI('/api/status'),
  getHealth: () => fetchAPI('/api/health'),
  getAgents: () => fetchAPI('/api/agents'),
  createAgent: (data: any) => fetchAPI('/api/agents', { method: 'POST', body: JSON.stringify(data) }),
  startAgents: () => fetchAPI('/api/agents/start', { method: 'POST' }),
  stopAgents: () => fetchAPI('/api/agents/stop', { method: 'POST' }),
  getMarketData: (symbol = 'SOL/USD') => fetchAPI(`/api/market?symbol=${symbol}`),
  getSignals: (symbol = 'SOL/USD') => fetchAPI(`/api/signals?symbol=${symbol}`),
  getStrategies: () => fetchAPI('/api/strategies'),
  runBacktest: (strategy = 'momentum', days = 365) =>
    fetchAPI('/api/backtest', { method: 'POST', body: JSON.stringify({ strategy, days }) }),
  getPositions: () => fetchAPI('/api/positions'),
  getOrders: () => fetchAPI('/api/orders'),
  createWallet: () => fetchAPI('/api/wallet/create', { method: 'POST' }),
  getWalletStatus: () => fetchAPI('/api/wallet/status'),
  getSkills: () => fetchAPI('/api/skills'),
  getSimulationData: () => fetchAPI('/api/simulation'),
}
