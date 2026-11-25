import { request } from './client'

export function createComment(postId, payload) {
  return request(`/api/posts/${postId}/comments`, { method: 'POST', body: payload })
}

export function deleteComment(commentId) {
  return request(`/api/comments/${commentId}`, { method: 'DELETE' })
}
