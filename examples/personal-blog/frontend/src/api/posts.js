import { request } from './client'

export function listPosts({ limit = 20, offset = 0 } = {}) {
  return request(`/api/posts?limit=${limit}&offset=${offset}`)
}

export function getPost(idOrSlug) {
  return request(`/api/posts/${encodeURIComponent(idOrSlug)}`)
}

export function createPost(payload) {
  return request('/api/posts', { method: 'POST', body: payload })
}

export function updatePost(id, payload) {
  return request(`/api/posts/${id}`, { method: 'PUT', body: payload })
}

export function deletePost(id) {
  return request(`/api/posts/${id}`, { method: 'DELETE' })
}

export function togglePin(id) {
  return request(`/api/posts/${id}/pin`, { method: 'PATCH' })
}
