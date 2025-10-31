import { createRouter, createWebHistory } from 'vue-router'
import LaureatesView from '@/views/LaureatesView.vue'
import PrizesView from '@/views/PrizesView.vue'

const routes = [
  { path: '/', redirect: '/laureats' },
  { path: '/laureats', name: 'Laureates', component: LaureatesView },
  { path: '/prizes', name: 'Prizes', component: PrizesView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})