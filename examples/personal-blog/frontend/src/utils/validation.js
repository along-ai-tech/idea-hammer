const LIMITS = { nickname: 50, comment: 5000, title: 200 }

export function validateComment({ nickname, content }) {
  const errors = {}
  const nick = (nickname || '').trim()
  const text = (content || '').trim()
  if (!nick) {
    errors.nickname = '昵称不能为空'
  } else if (nick.length > LIMITS.nickname) {
    errors.nickname = `昵称不能超过 ${LIMITS.nickname} 字`
  }
  if (!text) {
    errors.content = '评论内容不能为空'
  } else if (text.length > LIMITS.comment) {
    errors.content = `评论内容不能超过 ${LIMITS.comment} 字`
  }
  return { valid: Object.keys(errors).length === 0, errors }
}

export function validatePost({ title, content }) {
  const errors = {}
  const head = (title || '').trim()
  const text = (content || '').trim()
  if (!head) {
    errors.title = '标题不能为空'
  } else if (head.length > LIMITS.title) {
    errors.title = `标题不能超过 ${LIMITS.title} 字`
  }
  if (!text) {
    errors.content = '正文不能为空'
  }
  return { valid: Object.keys(errors).length === 0, errors }
}
