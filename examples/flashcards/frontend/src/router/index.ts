import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CardsView from '@/views/CardsView.vue'
import StudyView from '@/views/StudyView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/cards', name: 'cards', component: CardsView },
    { path: '/study', name: 'study', component: StudyView }
  ]
})

export default router
