<template>
  <div id="app" style="display:flex;flex-direction:column;">
    <AppHeader :isLogin="isLogin" :userName="userName"></AppHeader>
    <router-view style="text-align: center;margin-top:4px;flex:1;"/>
    <AppFooter></AppFooter>
  </div>
</template>

<style>
html,body,#app{
  height: 100%;
  min-height: 100%;
  width: 100%;
  margin: 0;
}

</style>


<script>
import AppHeader from './components/Header.vue';
import AppFooter from './components/Footer.vue';
export default {
  components:{
    AppHeader,
    AppFooter,
  },
  data() {
    return {
      isLogin: false,
      userName:'',
    }
  },
  created: function(){
    document.title = this.$route.meta.title || this.$route.meta.pathName
  },
  updated: function() {
    this.isLogin = sessionStorage.getItem('loginStatus');
    this.userName = sessionStorage.getItem('userName');
    //console.log('=== updated', this.isLogin, this.userName);
  },
  watch:{
    $route(){
      document.title = this.$route.meta.title || this.$route.meta.pathName
    }
  },
  methods: {
  }
};
</script>