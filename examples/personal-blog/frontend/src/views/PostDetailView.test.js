import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import PostDetailView from './PostDetailView.vue'
import { getPost } from '../api/posts'
import { createComment } from '../api/comments'
import { reactToPost } from '../api/reactions'

vi.mock('../api/posts', () => ({ getPost: vi.fn() }))
vi.mock('../api/comments', () => ({ createComment: vi.fn() }))
vi.mock('../api/reactions', () => ({ reactToPost: vi.fn() }))

const detail = {
  id: 1,
  title: '测试文章',
  content: '正文内容',
  is_pinned: false,
  created_at: '2026-01-01T00:00:00',
  comments: [],
  up_count: 0,
  down_count: 0,
}

function mountDetail() {
  return mount(PostDetailView, {
    props: { id: '1' },
    global: { plugins: [ElementPlus] },
  })
}

describe('PostDetailView', () => {
  beforeEach(() => {
    getPost.mockReset()
    createComment.mockReset()
    reactToPost.mockReset()
    getPost.mockResolvedValue({ ...detail })
  })

  // @trace TEST-034 REQ-003/AC-003-01
  it('submits a comment and appends it to the list', async () => {
    createComment.mockResolvedValue({
      id: 9,
      post_id: 1,
      nickname: 'alice',
      content: '学到了',
      created_at: '2026-01-02T00:00:00',
    })

    const wrapper = mountDetail()
    await flushPromises()

    await wrapper.find('input').setValue('alice')
    await wrapper.find('textarea').setValue('学到了')
    await wrapper.find('[data-test="submit-comment"]').trigger('click')
    await flushPromises()

    expect(createComment).toHaveBeenCalledWith(1, { nickname: 'alice', content: '学到了' })
    expect(wrapper.text()).toContain('alice')
    expect(wrapper.text()).toContain('学到了')
  })

  // @trace TEST-035 REQ-004/AC-004-01
  it('updates counts from the reaction response', async () => {
    reactToPost.mockResolvedValue({ post_id: 1, up_count: 9, down_count: 1, my_reaction: 'up' })

    const wrapper = mountDetail()
    await flushPromises()

    await wrapper.find('[data-test="react-up"]').trigger('click')
    await flushPromises()

    expect(reactToPost).toHaveBeenCalledWith(1, 'up')
    expect(wrapper.find('[data-test="react-up"]').text()).toContain('9')
    expect(wrapper.find('[data-test="react-down"]').text()).toContain('1')
  })
})
