const BASE = import.meta.env.VITE_API_BASE || ''

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function detailToMessage(detail) {
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || '参数不合法').join('；')
  }
  return typeof detail === 'string' ? detail : '请求失败'
}

export async function request(path, { method = 'GET', body, headers = {} } = {}) {
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers: body === undefined ? headers : { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (response.status === 204) return null
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new ApiError(detailToMessage(data && data.detail), response.status)
  }
  return data
}
