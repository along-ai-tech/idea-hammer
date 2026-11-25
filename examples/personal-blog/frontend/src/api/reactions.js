import { request } from './client'

export function reactToPost(postId, type) {
  return request(`/api/posts/${postId}/react`, { method: 'POST', body: { type } })
}

export function getReactions(postId) {
  return request(`/api/posts/${postId}/reactions`)
}
