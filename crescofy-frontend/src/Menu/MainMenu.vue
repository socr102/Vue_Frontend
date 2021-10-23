<template>
  <!-- leftbar-tab-menu -->
  <div class="leftbar-tab-menu">
    <div class="main-icon-menu">
      <router-link :to="{name: 'Dashboard'}" class="logo logo-metrica d-block text-center">
        <span>
          <img src="@/../public/assets/images/logo-sq.png" alt="logo-small" class="logo-sm">
        </span>
      </router-link>
      <nav class="nav" v-if="userProfile.email">
        <router-link :to="{name: 'Dashboard'}" class="nav-left-bar" title="Home Page">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-monitor align-self-center menu-icon icon-dual">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
          </svg>
        </router-link>
        <router-link :to="{name: 'Dashboard'}">Dashboard</router-link>
        <router-link :to="{name: 'ArticleAnalysis'}" class="nav-left-bar" title="Articles Analysis">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-grid align-self-center menu-icon icon-dual">
            <rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>
          </svg>
        </router-link>
        <router-link :to="{name: 'ArticleAnalysis'}">Analytics</router-link>
        <router-link :to="{name: 'CartComposition'}" class="nav-left-bar" title="Cart Composition">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-shopping-cart align-self-center menu-icon icon-dual">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
        </router-link>
        <router-link :to="{name: 'CartComposition'}">Cart</router-link>
        <router-link :to="{name: 'Offers'}" class="nav-left-bar" title="Cart Composition">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7081b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-gift align-self-center menu-icon icon-dual">
            <polyline points="20 12 20 22 4 22 4 12"></polyline>
            <rect x="2" y="7" width="20" height="5"></rect>
            <line x1="12" y1="22" x2="12" y2="7"></line>
            <path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path>
            <path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path>
          </svg>
        </router-link>
        <router-link :to="{name: 'Offers'}">Offers</router-link>
        <router-link :to="{name: 'Audience'}" class="nav-left-bar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7081b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-users">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </router-link>
        <router-link :to="{name: 'Audience'}">Audience</router-link>
        <router-link :to="{name: 'Campaigns'}" class="nav-left-bar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7081b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-shopping-bag">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
        </router-link>
        <router-link :to="{name: 'Campaigns'}">Campaigns</router-link>
        <router-link :to="{name: 'Members'}" class="nav-left-bar">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7081b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="feather feather-user-check">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="8.5" cy="7" r="4"></circle>
            <polyline points="17 11 19 13 23 9"></polyline>
          </svg>
        </router-link>
        <router-link :to="{name: 'Members'}">Members</router-link>
      </nav>
    </div><!--end main-icon-menu-->
  </div>
  <!-- end leftbar-tab-menu-->
</template>

<script>
import { mapGetters } from 'vuex';


export default {
  name: 'MainMenu',
  computed: {
    ...mapGetters('user', {userProfile: 'userProfile'})
  }
}
</script>

<style>
.nav-left-bar {
  padding-top: 25px;
}
</style>
