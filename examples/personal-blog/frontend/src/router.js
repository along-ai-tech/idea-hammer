import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import PostDetailView from './views/PostDetailView.vue'
import AdminView from './views/AdminView.vue'
import PostEditorView from './views/PostEditorView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/posts', name: 'posts', component: HomeView },
  { path: '/posts/:id', name: 'post-detail', component: PostDetailView, props: true },
  { path: '/admin', name: 'admin', component: AdminView },
  { path: '/admin/new', name: 'post-new', component: PostEditorView },
  { path: '/admin/posts/:id/edit', name: 'post-edit', component: PostEditorView, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
