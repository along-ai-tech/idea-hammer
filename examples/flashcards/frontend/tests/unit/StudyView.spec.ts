import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

import StudyView from '@/views/StudyView.vue'
import { api } from '@/api'

vi.mock('@/api', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

const elStubs = {
  'el-card': { template: '<div class="el-card"><slot /></div>' },
  'el-button': { props: ['type', 'size'], template: '<button class="el-btn"><slot /></button>' },
  'el-button-group': { template: '<div class="el-btn-group"><slot /></div>' },
  'el-empty': { props: ['description'], template: '<div class="el-empty">{{ description }}<slot /></div>' },
  'el-alert': { props: ['title', 'type'], template: '<div class="el-alert">{{ title }}</div>' },
  'el-link': { props: ['type', 'href'], template: '<a class="el-link"><slot /></a>' },
  'router-link': { props: ['to'], template: '<a><slot /></a>' },
}

const mockQueue = [
  { id: 1, front: 'Question 1', back: 'Answer 1', repetitions: 0, interval: 0, easiness_factor: 2.5, due_at: null, last_reviewed_at: null },
]

function mountStudyView() {
  return mount(StudyView, {
    global: {
      plugins: [createPinia()],
      stubs: elStubs,
    },
  })
}

describe('StudyView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('挂载时应调用 fetchQueue 加载复习队列', async () => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockQueue })
    mountStudyView()
    await flushPromises()
    expect(api.get).toHaveBeenCalledWith('/study/queue')
  })

  it('加载完成后应渲染卡片正面', async () => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockQueue })
    const wrapper = mountStudyView()
    await flushPromises()
    expect(wrapper.text()).toContain('Question 1')
    expect(wrapper.text()).toContain('显示答案')
  })

  it('点击"显示答案"按钮应渲染卡片反面（含答案和评分按钮）', async () => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockQueue })
    const wrapper = mountStudyView()
    await flushPromises()
    const revealBtn = wrapper.findAll('button').find((b) => b.text().includes('显示答案'))
    expect(revealBtn).toBeTruthy()
    await revealBtn!.trigger('click')
    await flushPromises()
    expect(wrapper.text()).toContain('Answer 1')
    // 6 个评分按钮 0-5
    const ratingBtns = wrapper.findAll('button').filter((b) => /^[0-5]$/.test(b.text().trim()))
    expect(ratingBtns.length).toBe(6)
  })

  it('点击评分按钮 3 应调用 POST /study/1/review {quality:3}', async () => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: mockQueue })
    vi.mocked(api.post).mockResolvedValueOnce({ data: {} })
    const wrapper = mountStudyView()
    await flushPromises()
    // 翻到答案面
    const revealBtn = wrapper.findAll('button').find((b) => b.text().includes('显示答案'))
    await revealBtn!.trigger('click')
    await flushPromises()
    // 点评分 3
    const rateBtn = wrapper.findAll('button').find((b) => b.text().trim() === '3')
    expect(rateBtn).toBeTruthy()
    await rateBtn!.trigger('click')
    await flushPromises()
    expect(api.post).toHaveBeenCalledWith('/study/1/review', { quality: 3 })
  })

  it('队列为空时应显示"今日复习完毕"状态', async () => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: [] })
    const wrapper = mountStudyView()
    await flushPromises()
    expect(wrapper.text()).toContain('今日复习完毕')
  })
})
