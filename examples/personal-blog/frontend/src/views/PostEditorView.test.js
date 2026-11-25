import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import PostEditorView from './PostEditorView.vue'
import { createPost } from '../api/posts'

const { push } = vi.hoisted(() => ({ push: vi.fn() }))

vi.mock('vue-router', () => ({ useRouter: () => ({ push }) }))
vi.mock('../api/posts', () => ({
  createPost: vi.fn(),
  getPost: vi.fn(),
  updatePost: vi.fn(),
}))

describe('PostEditorView', () => {
  beforeEach(() => {
    push.mockReset()
    createPost.mockReset()
  })

  // @trace TEST-038 REQ-001/AC-001-01
  it('creates a post and navigates back to admin', async () => {
    createPost.mockResolvedValue({ id: 1, title: '新文章', content: '正文' })

    const wrapper = mount(PostEditorView, {
      global: { plugins: [ElementPlus] },
    })

    await wrapper.find('input').setValue('新文章')
    await wrapper.find('textarea').setValue('正文')
    await wrapper.find('[data-test="save-post"]').trigger('click')
    await flushPromises()

    expect(createPost).toHaveBeenCalledWith({
      title: '新文章',
      content: '正文',
      is_pinned: false,
    })
    expect(push).toHaveBeenCalledWith('/admin')
  })
})
