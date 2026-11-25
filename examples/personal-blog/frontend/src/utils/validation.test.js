import { describe, expect, it } from 'vitest'
import { validateComment, validatePost } from './validation'

describe('validation', () => {
  // @trace TEST-030 REQ-003/AC-003-02
  it('rejects empty comment nickname and content', () => {
    const result = validateComment({ nickname: '   ', content: '' })
    expect(result.valid).toBe(false)
    expect(result.errors.nickname).toBe('昵称不能为空')
    expect(result.errors.content).toBe('评论内容不能为空')

    const ok = validateComment({ nickname: 'alice', content: '学到了' })
    expect(ok.valid).toBe(true)
  })

  // @trace TEST-031 REQ-001/AC-001-02
  it('rejects empty post title and content', () => {
    const empty = validatePost({ title: '', content: '' })
    expect(empty.valid).toBe(false)
    expect(empty.errors.title).toBe('标题不能为空')
    expect(empty.errors.content).toBe('正文不能为空')

    const longTitle = validatePost({ title: 'a'.repeat(201), content: 'x' })
    expect(longTitle.errors.title).toContain('200')
  })
})
