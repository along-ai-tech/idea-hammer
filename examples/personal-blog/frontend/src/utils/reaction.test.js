import { describe, expect, it } from 'vitest'
import { applyReaction } from './reaction'

describe('applyReaction', () => {
  // @trace TEST-032 REQ-004/AC-004-02
  it('increments, switches and ignores repeated same type', () => {
    const first = applyReaction({ up: 0, down: 0, mine: '' }, 'up')
    expect(first).toEqual({ up: 1, down: 0, mine: 'up' })

    const switched = applyReaction(first, 'down')
    expect(switched).toEqual({ up: 0, down: 1, mine: 'down' })

    const repeated = applyReaction(switched, 'down')
    expect(repeated).toEqual({ up: 0, down: 1, mine: 'down' })
  })
})
