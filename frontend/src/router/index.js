import {createRouter, createWebHistory} from 'vue-router'
import Metrics from '../views/Metrics.vue'
import Analyze from '../views/Analyze.vue'
import Settings from '../views/Settings.vue'
import Login from '../views/Login.vue'
import Callback from '../views/Callback.vue'
import Slack2 from '../views/Slack2.vue'
import Logout from '../views/Logout.vue'

// Vue.use(VueRouter)

const routerHistory = createWebHistory()

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Metrics
  },
  {
    path: '/metrics',
    name: 'Metrics',
    component: Metrics
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: Analyze
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/team',
    name: 'Team',
    component: Settings
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/slack2',
    name: 'Slack2',
    component: Slack2
  },
  {
    path: '/callback',
    name: 'Callback',
    component: Callback
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
]

const router = new createRouter({
  mode: 'history',
  history: routerHistory,
  base: process.env.BASE_URL,
  routes: routes
})

export default router
