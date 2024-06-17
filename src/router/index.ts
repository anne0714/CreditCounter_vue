import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MajorView from '../views/MajorView.vue'
import MyClass from '../views/MyClass.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Module from '../views/Module.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/major', component: MajorView },
  { path: '/myclass', component: MyClass },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/module', component: Module },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
