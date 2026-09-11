import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

import { api } from '@/api'
import { useStudyStore } from '@/stores/study'

vi.mock('@/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

describe('useStudyStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('初始 queue 应为空数组而非 undefined', () => {
    const store = useStudyStore()
    expect(store.queue).toEqual([])
  })

  it('初始 currentIndex 应为 0', () => {
    const store = useStudyStore()
    expect(store.currentIndex).toBe(0)
  })

  it('fetchQueue 成功后 queue 应填充响应数据并清空 error', async () => {
    const mockCards = [
      { id: 1, front: 'A', back: 'a' },
      { id: 2, front: 'B', back: 'b' },
    ]
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockCards })
    const store = useStudyStore()
    await store.fetchQueue()
    expect(api.get).toHaveBeenCalledWith('/study/queue')
    expect(store.queue).toEqual(mockCards)
    expect(store.currentIndex).toBe(0)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('fetchQueue 失败应设置 error 且保持空 queue', async () => {
    vi.mocked(api.get).mockRejectedValueOnce(new Error('network down'))
    const store = useStudyStore()
    await store.fetchQueue()
    expect(store.queue).toEqual([])
    expect(store.error).toBe('network down')
    expect(store.loading).toBe(false)
  })

  it('fetchQueue 期间 loading 应为 true（同步前置状态）', () => {
    const store = useStudyStore()
    expect(store.loading).toBe(false)
    // 触发但不 await：观察同步 loading 状态
    vi.mocked(api.get).mockImplementationOnce(() => new Promise(() => {}))
    store.fetchQueue()
    expect(store.loading).toBe(true)
  })

  it('currentCard 返回当前索引的卡片', () => {
    const store = useStudyStore()
    store.queue = [
      { id: 1, front: 'A' },
      { id: 2, front: 'B' },
      { id: 3, front: 'C' },
    ] as any
    store.currentIndex = 1
    expect(store.currentCard).toEqual({ id: 2, front: 'B' })
  })

  it('currentCard 在越界时应返回 null', () => {
    const store = useStudyStore()
    store.queue = [{ id: 1, front: 'A' }] as any
    store.currentIndex = 5
    expect(store.currentCard).toBeNull()
  })

  it('nextCard 应让 currentIndex + 1', () => {
    const store = useStudyStore()
    store.queue = [{ id: 1 }, { id: 2 }] as any
    store.currentIndex = 0
    store.nextCard()
    expect(store.currentIndex).toBe(1)
  })

  it('isFinished 在 currentIndex 越过 queue 长度时为 true', () => {
    const store = useStudyStore()
    store.queue = [{ id: 1 }] as any
    store.currentIndex = 1
    expect(store.isFinished).toBe(true)
  })

  it('isFinished 在 queue 为空时为 true', () => {
    const store = useStudyStore()
    expect(store.isFinished).toBe(true)
  })

  it('progress 返回 当前/总数 字符串（1-based）', () => {
    const store = useStudyStore()
    store.queue = [{ id: 1 }, { id: 2 }, { id: 3 }] as any
    store.currentIndex = 1
    expect(store.progress).toBe('2 / 3')
  })

  it('progress 在 isFinished 时不超过总数', () => {
    const store = useStudyStore()
    store.queue = [{ id: 1 }, { id: 2 }] as any
    store.currentIndex = 2
    expect(store.progress).toBe('2 / 2')
  })

  it('submitReview 应调用 POST /study/{id}/review 带 quality', async () => {
    vi.mocked(api.post).mockResolvedValueOnce({ data: {} })
    const store = useStudyStore()
    store.queue = [{ id: 7, front: 'Q' }] as any
    store.currentIndex = 0
    await store.submitReview(4)
    expect(api.post).toHaveBeenCalledWith('/study/7/review', { quality: 4 })
  })

  it('submitReview 在 currentCard 为 null 时不应调用 api', async () => {
    const store = useStudyStore()
    store.queue = []
    store.currentIndex = 0
    await store.submitReview(3)
    expect(api.post).not.toHaveBeenCalled()
  })
})
