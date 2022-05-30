import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    meta:{title: 'Let\'s code - 算法竞赛开赛提醒聚合站', },
    component: Home
  },
  {
    path: '/calendar',
    name: 'Calendar',
    meta:{title: 'Let\'s code - 算法竞赛开赛提醒聚合站', },
    component: () => import('../views/Calendar.vue')
  },
  {
    path: '/subscribe',
    name: 'Subscribe',
    meta:{title: 'Let\'s code - 算法竞赛开赛提醒聚合站', },
    component: () => import('../views/Subscribe.vue')
  },
  {
    path: '/discussion',
    name: 'Discussion',
    meta:{title: 'Let\'s code - 算法竞赛开赛提醒聚合站', },
    component: () => import('../views/Discussion.vue')
  },
  {
    path: '/register',
    name: 'Register',
    meta:{title: '注册 - Let\'s code - 算法竞赛开赛提醒聚合站', },
    component: () => import('../views/Register.vue')
  },
  {
    path: '/login',
    name: 'Login',
    meta:{title: '登录 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/Login.vue')
  },
  {
    path: '/forgetpw',
    name: 'ForgetPassword',
    meta:{title: '忘记密码 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/Forgetpw.vue')
  },
  {
    path: '/user/resetpw',
    name: 'ResetPassword',
    meta:{title: '重设密码 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/User/Resetpw.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    meta:{title: '后台管理 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/Admin.vue')
  },
  {
    path: '/user/index',
    name: 'User',
    meta:{title: '个人主页 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/User/Index.vue')
  },
  {
    path: '/test',
    name: 'Test',
    meta:{title: '功能测试页面 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/Test.vue')
  },
  {
    path: '/404',
    name: '404',
    meta:{title: '乌乌，页面丢失了 - Let\'s code - 算法竞赛开赛提醒聚合站',},
    component: () => import('../views/404.vue')
  },
  {
    path: '*',    // 此处需特别注意至于最底部
    redirect: '/404'
  }
]

const router = new VueRouter({
  mode: "history",
  routes
})

router.beforeEach((to, from, next)=>{
  console.log("Check router");
  const token =sessionStorage.getItem('token');
  if ((to.path === '/login')||(to.path === '/register')) {
    if (token) {
      next('/')
      return
    }
    next()
    return
  }
  if (!token) {
    next('/login')
    return
  }
  next()
})

export default router
