// @ts-ignore  // 临时忽略找不到模块的类型声明错误
import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import HomeView from '@/views/HomeView.vue'
import ProjectList from '@/views/ProjectList.vue'
// @ts-ignore
import { ElMessage } from 'element-plus'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView
        },
        {
          path: 'projects',
          name: 'projects',
          component: ProjectList
        },
        {
          path: 'test-cases',
          name: 'test-cases',
          component: () => import('@/views/TestCaseList.vue')
        },
        {
          path: 'tasks',
          name: 'tasks',
          component: () => import('@/views/TaskList.vue')
        },
        {
          path: 'reports',
          name: 'reports',
          component: () => import('@/views/ReportList.vue')
        },
        {
          path: 'admin/users',
          name: 'admin-users',
          component: () => import('@/views/AdminUserList.vue'),
          meta: { requiresAdmin: true }
        }
      ]
    }
  ]
})

router.beforeEach((to: any, from: any, next: (to?: any) => void) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.name !== 'login' && to.name !== 'register' && !token) {
    next({ name: 'login' })
  } else if (to.meta.requiresAdmin && !user.is_superuser) {
    ElMessage.error('Access Denied')
    next(from.name ? false : { name: 'home' })
  } else {
    next()
  }
})

export default router
