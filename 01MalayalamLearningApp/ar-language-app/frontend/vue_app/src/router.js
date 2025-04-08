import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from './components/LandingPage.vue';
import PracticeScreen from './components/PracticeScreen.vue';

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: LandingPage 
  },
  { 
    path: '/practice', 
    name: 'Practice',
    component: PracticeScreen,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;