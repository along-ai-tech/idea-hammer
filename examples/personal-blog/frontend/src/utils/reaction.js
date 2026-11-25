export function applyReaction(counts, type) {
  const up = counts.up || 0
  const down = counts.down || 0
  const mine = counts.mine || ''
  if (mine === type) return { up, down, mine }

  const next = { up, down, mine: type }
  if (type === 'up') next.up += 1
  else next.down += 1
  if (mine === 'up') next.up -= 1
  if (mine === 'down') next.down -= 1
  return next
}
