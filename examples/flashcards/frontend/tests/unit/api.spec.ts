import { describe, it, expect } from 'vitest'
import { api } from '@/api'

describe('api client', () => {
  it('baseURL 应指向 /api 走 Vite 代理', () => {
    expect(api.defaults.baseURL).toBe('/api')
  })

  it('timeout 应配置为 10 秒', () => {
    expect(api.defaults.timeout).toBe(10000)
  })

  it('默认 Content-Type 应该是 JSON', () => {
    expect(api.defaults.headers['Content-Type']).toBe('application/json')
  })
})
