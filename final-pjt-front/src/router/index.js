// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ArticleCreateView from '../views/ArticleCreateView.vue';
import SignUpView from '@/views/SignUpView.vue';
import SignInView from '@/views/SignInView.vue';
import ExchangeView from '@/views/ExchangeView.vue';
import MyProfileView from '@/views/MyProfileView.vue';
import MyProfileUpdateView from '@/views/MyProfileUpdateView.vue';
import InterestProductsView from '@/views/InterestProductsView.vue';
import ArticleDetailView from '@/views/ArticleDetailView.vue';
import ArticleUpdateView from '@/views/ArticleUpdateView.vue';
import { useUserStore } from '@/stores/user.js';
import MapView from '@/views/MapView.vue'
import FinanceView from '@/views/FinanceView.vue'
import FinanceDepositList from '@/components/FinanceDepositList.vue'
import FinanceSavingList from '@/components/FinanceSavingList.vue'
import CGPTView from '@/views/CGPTView.vue'
import CompareProduct from '@/components/CompareProduct.vue'
import CommunityView from '@/views/CommunityView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/create',
      name: 'create',
      component: ArticleCreateView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },
    {
      path: '/myprofile',
      name: 'myprofile',
      component: MyProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/articles/:id',
      name: 'articleDetail',
      component: ArticleDetailView,
    },
    {
      path: '/articles/:id/update',
      name: 'articleUpdate',
      component: ArticleUpdateView,
    },
    {
      path: '/myprofile/update',
      name: 'myprofileupdate',
      component: MyProfileUpdateView,
      meta: { requiresAuth: true }
    },
    {
      path: '/map',
      name: 'map',
      component: MapView
    },
    {
      path: '/finance',
      name: 'finance',
      component: FinanceView,
      children: [
        {
          path: 'deposit',
          name: 'depositList',
          component: FinanceDepositList
        },
        {
          path: 'saving',
          name: 'savingList',
          component: FinanceSavingList
        }
      ]
    },
    {
      path: '/cgpt',
      name: 'cgpt',
      component: CGPTView
    }, 
    {
      path: '/myprofile/interest-products',
      name: 'InterestProductsView',
      component: InterestProductsView,
    },
    {
      path: '/recommend/',
      name: 'recommend',
      component: CompareProduct,
    },
    {
      path: '/community/',
      name: 'community',
      component: CommunityView,
    },
  ]
});

router.beforeEach((to, from, next) => {
  const store = useUserStore();
  if (to.meta.requiresAuth && !store.isLogin) {
    window.alert('로그인이 필요합니다.');
    next({ name: 'signin' });
  } else if ((to.name === 'signup' || to.name === 'signin') && store.isLogin) {
    window.alert('로그인이 되어 있습니다.');
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router;
