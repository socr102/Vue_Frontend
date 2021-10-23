import { createApp } from 'vue';
import { configure } from 'vee-validate';
import axios from 'axios';

import App from './App.vue';
import {store} from '@/Core/store/index';
import router from './Router';
import {LOGOUT} from '@/Core/store/action-types';
import {ability, defineRulesFor} from '@/Core/helpers/ability';
import alertify from 'alertifyjs'
import VueApexCharts from "vue3-apexcharts";


configure({
  validateOnBlur: true, // controls if `blur` events should trigger validation with `handleChange` handler
  validateOnChange: true, // controls if `change` events should trigger validation with `handleChange` handler
  validateOnInput: true, // controls if `input` events should trigger validation with `handleChange` handler
  validateOnModelUpdate: true, // controls if `update:modelValue` events should trigger validation with `handleChange` handler
});

// 401 Unauthorized Error interceptors
axios.interceptors.response.use(function (response) {
  return response;
}, function (error) {
  let isLogin = router.currentRoute.value.name == 'Login';
  if (error.response.status == 401 && !isLogin) {
    // Remove User Profile data and redirecting to login page
    store.dispatch(`user/${LOGOUT}`,
                   app.config.globalProperties.$ability);
    router.push('/login');
  }
  return Promise.reject(error);
});

var app = createApp(App);

app.config.globalProperties.$ability = ability.update(
  defineRulesFor(store.state.user.userProfile));
router.$global = app.config.globalProperties;

alertify.set('notifier','position', 'top-center');
app.config.globalProperties.$alertify = alertify;

app
  .use(store)
  .use(router)
  .use(VueApexCharts)
  .mount('#app')
