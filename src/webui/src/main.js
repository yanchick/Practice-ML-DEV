import Vue from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from '.';

Vue.config.productionTip = false;

Vue.prototype.$axios = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your backend API URL
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !token) {
    // Redirect to login if trying to access a protected route without a token
    next('/login');
  } else {
    next();
  }
});

new Vue({
  render: (h) => h(App),
  router,
}).$mount('#app');
