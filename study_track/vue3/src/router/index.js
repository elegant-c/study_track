import { createRouter, createWebHashHistory } from "vue-router";
import register from "../view/register.vue";
import Conversation from '../view/Conversation.vue';
import Conversation2 from '../view/Conversation2.vue';
import Conversation3 from '../view/Conversation3.vue';
import Conversation4 from '../view/Conversation4.vue';
import PersonalCenter from '../view/PersonalCenter.vue';
import TrendAnalysis from '../view/TrendAnalysis.vue';
import GradeManagement from '../view/GradeManagement.vue';
import LearningAdvice from '../view/LearningAdvice.vue';
import start from "../view/start.vue";

const routes = [
  {
    path: '/',
    redirect: '/start', // 重定向根路径到 /start
  },
  {
    path: '/start',
    name: 'start',
    component: start,
  },
  {
    path: "/login",
    name: "login",
    meta: {
      title: "登录",
    },
    component: () => import("../view/login.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: register,
  },
  {
    path: "/home",
    name: "主页",
    meta: {
      title: "主页",
    },
    component: () => import("../view/home.vue"),
    redirect: "/index",
    children: [
      {
        path: "/index",
        name: "index",
        meta: {
          title: "首页",
        },
        component: () => import("../view/welcome.vue"),
      },
    ],
  },
  {
    path: '/conversation',
    name: 'conversation',
    component: Conversation,
  },
  {
    path: '/conversation2',
    name: 'conversation2',
    component: Conversation2,
  },
  {
    path: '/conversation3',
    name: 'conversation3',
    component: Conversation3,
  },
  {
    path: '/conversation4',
    name: 'conversation4',
    component: Conversation4,
  },
  {
    path: '/trend-analysis',
    name: 'TrendAnalysis',
    component: TrendAnalysis
  },
  {
    path: '/grade-management',
    name: 'GradeManagement',
    component: GradeManagement
  },
  {
    path: '/learning-advice',
    name: 'LearningAdvice',
    component: LearningAdvice
  },
  {
    path: '/personal-center',
    name: 'PersonalCenter',
    component: PersonalCenter
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 修改页面 title
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = "成绩通 - " + to.meta.title;
  }
  
  // 放行所有路由，不再进行动态路由添加的判断
  next();
});

// 导出路由
export default router;