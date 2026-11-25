import { afterEach, describe, expect, it, vi } from 'vitest'
import { ApiError, request } from './client'

describe('api client', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  // @trace TEST-029 REQ-001/AC-001-02
  it('sends JSON and normalizes 422 detail into ApiError', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [{ id: 1 }],
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 422,
        json: async () => ({ detail: [{ msg: '标题不能为空' }] }),
      })
    vi.stubGlobal('fetch', fetchMock)

    const data = await request('/api/posts')
    expect(data).toEqual([{ id: 1 }])

    await expect(request('/api/posts', { method: 'POST', body: { title: '' } }))
      .rejects.toBeInstanceOf(ApiError)
    expect(fetchMock).toHaveBeenLastCalledWith('/api/posts', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ title: '' }),
    }))
  })
})
