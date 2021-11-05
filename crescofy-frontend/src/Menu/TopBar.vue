<template>
  <!-- <div id="header" v-if="userProfile.email"> -->
  <div id="header" >

    <button class="toggle-btn" @click="toggleFun()"></button>
    <div class="title-details">
      <h2>{{title}}</h2>
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="#"></a></li>
          <!-- <li class="breadcrumb-item"><a href="#">{{auth.dashboard}}</a></li> -->

          <!-- <li class="breadcrumb-item active" aria-current="page">{{author.cart}}</li> -->
          <li class="breadcrumb-item active" aria-current="page"></li>
          <!-- <li class="breadcrumb-item active" aria-current="page">Library</li> -->
        </ol>
      </nav>
    </div>
    <div v-if="currentUrl == '/Cart'" id="product-tabs">
      <div class="toolbar-holder p-2" >
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb p-2">
              <li class="breadcrumb-item">Sort by</li>
            </ol>
          </nav>
          <div class=" select-holder "   >
              <select class="nav-dropdown">
                <option>Most Common Combinations</option>
                <option>Most Common Combinations</option>
                <option>Most Common Combinations</option>
                <option>Most Common Combinations</option>
              </select>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { LOGOUT } from '@/Core/store/action-types';
import { UserRoleMixin } from '@/Core/mixins/UserRoleMixin';

export default {
  name: 'TopBar',
  computed: {
    ...mapGetters('user', ['userProfile'])
  },
  mixins: [UserRoleMixin],
  methods: {
    ...mapActions('user', [LOGOUT]),
    signOut() {
      this[LOGOUT](this.$ability);
      this.$router.push('/login');
    }
  }
}
</script>

<style>
.head-logo {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}
</style>
