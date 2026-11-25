import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import HomeView from './HomeView.vue'
import { listPosts } from '../api/posts'

vi.mock('../api/posts', () => ({ listPosts: vi.fn() }))

const routerLinkStub = { template: '<a><slot /></a>' }

function mountHome() {
  return mount(HomeView, {
    global: {
      plugins: [ElementPlus],
      stubs: { 'router-link': routerLinkStub },
    },
  })
}

describe('HomeView', () => {
  beforeEach(() => {
    listPosts.mockReset()
  })

  // @trace TEST-033 REQ-002/AC-002-01
  it('renders pinned post first with pinned marker', async () => {
    listPosts.mockResolvedValue([
      {
        id: 1,
        title: '置顶篇',
        content: '置顶内容',
        is_pinned: true,
        created_at: '2026-01-01T00:00:00',
      },
      {
        id: 2,
        title: '普通篇',
        content: '普通内容',
        is_pinned: false,
        created_at: '2026-01-02T00:00:00',
      },
    ])

    const wrapper = mountHome()
    await flushPromises()

    expect(listPosts).toHaveBeenCalledWith({ limit: 5, offset: 0 })
    const cards = wrapper.findAll('.post-card')
    expect(cards).toHaveLength(2)
    expect(cards[0].text()).toContain('置顶篇')
    expect(cards[0].classes()).toContain('pinned')
  })
})
