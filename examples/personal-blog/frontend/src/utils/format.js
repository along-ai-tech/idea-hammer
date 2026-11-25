export function formatDate(value) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN', { hour12: false })
}

export function excerpt(content, max = 80) {
  const text = (content || '').replace(/\s+/g, ' ').trim()
  return text.length > max ? `${text.slice(0, max)}…` : text
}

export function reactionSummary(up, down) {
  return `👍 ${up} · 👎 ${down}`
}
