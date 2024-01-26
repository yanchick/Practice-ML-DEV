import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

import Home from './components/Home.vue';
import Predictor from './components/Predictor.vue';
import Models from './components/Models.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/predictor', component: Predictor },
  { path: '/models', component: Models },
];


const router = new VueRouter({
  routes,
});

export default router;

