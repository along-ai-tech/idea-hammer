import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import AdminView from './AdminView.vue'
import { deletePost, listPosts, togglePin } from '../api/posts'

vi.mock('../api/posts', () => ({
  listPosts: vi.fn(),
  deletePost: vi.fn(),
  togglePin: vi.fn(),
}))

function mountAdmin() {
  return mount(AdminView, {
    global: { plugins: [ElementPlus] },
  })
}

describe('AdminView', () => {
  beforeEach(() => {
    listPosts.mockReset()
    deletePost.mockReset()
    togglePin.mockReset()
    listPosts.mockResolvedValue([
      { id: 1, title: '要置顶的文章', content: 'x', is_pinned: false, created_at: '2026-01-01T00:00:00' },
      { id: 2, title: '要删除的文章', content: 'y', is_pinned: false, created_at: '2026-01-02T00:00:00' },
    ])
  })

  // @trace TEST-036 REQ-005/AC-005-01
  it('toggles pin state in the row', async () => {
    togglePin.mockResolvedValue({ id: 1, title: '要置顶的文章', is_pinned: true })

    const wrapper = mountAdmin()
    await flushPromises()

    await wrapper.findAll('[data-test="pin-post"]')[0].trigger('click')
    await flushPromises()

    expect(togglePin).toHaveBeenCalledWith(1)
    expect(wrapper.findAll('[data-test="pin-post"]')[0].text()).toContain('取消置顶')
  })

  // @trace TEST-037 REQ-001/AC-001-03
  it('deletes a post and removes the row', async () => {
    deletePost.mockResolvedValue(null)

    const wrapper = mountAdmin()
    await flushPromises()

    await wrapper.findAll('[data-test="delete-post"]')[1].trigger('click')
    await flushPromises()

    expect(deletePost).toHaveBeenCalledWith(2)
    expect(wrapper.text()).not.toContain('要删除的文章')
    expect(wrapper.text()).toContain('要置顶的文章')
  })
})
