<template>
  <!-- leftbar-tab-menu -->
  <div id="sidebar">
      <div class="logo">
        <img src="@/../public/assets/images/logo1.png" alt="Logo" />
      </div>
      <div class="d-flex justify-content-between flex-column navigations" v-if="userProfile.email">
      
        <ul class="list-unstyled" >
            <router-link to="/dashboard" active-class="active ">
            <li class="icon-hov" >
            <DashboardIcon/> Dashboard
              </li>
            </router-link>
            <li class="icon-hov"><AnalyticsIcon />Analytics</li>
            <!-- <router-link to="Cart" active-class="active "> -->
            <li class="nav-item" ><CartIcon />Cart</li>
            <!-- </router-link> -->
            <!-- <router-link to="Offers"> -->
            <li class="icon-hov"><OfferIcon />Offers</li>
            <!-- </router-link> -->
            <!-- <router-link to="Campaigns"> -->
            <li class="icon-hov"><CampaignIcon />Campaigns</li>
            <!-- </router-link> -->
            <li class="icon-hov"><MembersIcon />Members</li>
            <li class="icon-hov"><AudienceIcon />Audience</li>
        </ul>
        <ul class="list-unstyled bottom-navigation">
            <li>
              <div class="user">
                <div class="image">
                  <img src="@/../public/assets/images/user.png" alt="User" />
                </div>
                <div class="name">userwitre</div>
                <span>Admin</span>
              </div>
            </li>
            <router-link to="Admins">
            <li class="icon-hov"><AdminIcon />Admins</li>
            </router-link>
        </ul>
      </div>
  </div>
  <!-- end leftbar-tab-menu-->
</template>

<script>
import { mapGetters } from 'vuex';
import DashboardIcon from '../icons/dashboard.vue'
import AnalyticsIcon from '../icons/analytics.vue'
import CartIcon from '../icons/cart.vue'
import OfferIcon from '../icons/offers.vue'
import CampaignIcon from '../icons/campaigns.vue'
import MembersIcon from '../icons/members.vue'
import AudienceIcon from '../icons/audience.vue'
import AdminIcon from '../icons/admins.vue'

export default {
  name: 'MainMenu',
  components: {
    DashboardIcon,
    AnalyticsIcon,
    CartIcon,
    OfferIcon,
    CampaignIcon,
    MembersIcon,
    AudienceIcon,
    AdminIcon
  },
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
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navigations {
  overflow: scroll;
}
</style>
