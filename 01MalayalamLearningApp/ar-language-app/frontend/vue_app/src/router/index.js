import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/LandingPage.vue'
import PracticeScreen from '@/components/PracticeScreen.vue'
import AlphabetScreen from '../components/AlphabetScreen.vue'
import MoviePlotScreen from '../components/MoviePlotScreen.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage
  },
  {
    path: '/practice',
    name: 'Practice',
    component: PracticeScreen
  },
  {
    path: '/alphabets',
    name: 'Alphabets',
    component: () => import('@/components/AlphabetScreen.vue')
  },
  {
    path: '/movie-plot',
    name: 'MoviePlot',
    component: () => import('@/components/MoviePlotScreen.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/components/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router