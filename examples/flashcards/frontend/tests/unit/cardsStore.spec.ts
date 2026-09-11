import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCardsStore } from '@/stores/cards'

describe('cardsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('初始状态应该是空数组而非 undefined', () => {
    const store = useCardsStore()
    expect(store.cards).toEqual([])
  })

  it('初始 loading 应该是 false', () => {
    const store = useCardsStore()
    expect(store.loading).toBe(false)
  })

  it('初始 error 应该是 null', () => {
    const store = useCardsStore()
    expect(store.error).toBeNull()
  })
})
