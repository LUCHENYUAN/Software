import Vue from 'vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)

//Vue.prototype.axios = axios
Vue.config.productionTip = false

Vue.use(Antd);

new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  router,
  store,
  render: h => h(App)
}).$mount('#app')


