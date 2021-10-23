<template>
  <div class="mm-active active mm-show enlarge-menu">
    <MainMenu/>
    <TopBar/>
    <router-view />
  </div>
</template>

<script>
import TopBar from '@/Menu/TopBar.vue';
import MainMenu from '@/Menu/MainMenu.vue';


export default {
  name: 'App',
  components: {
    TopBar,
    MainMenu
  }
}
</script>

<style>
@import '../node_modules/alertifyjs/build/css/alertify.min.css';
@import '../node_modules/alertifyjs/build/css/themes/default.min.css';
@import '../node_modules/alertifyjs/build/css/themes/bootstrap.min.css';
</style>
