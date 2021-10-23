<template>
<div>
<div class="topbar">
    <nav class="navbar-custom">
        <img src="@/../public/assets/images/logo.png" class="head-logo" height="54">
        <ul class="list-unstyled topbar-nav float-right mb-0">
            <li class="dropdown" v-if="userProfile.email">
                <a class="nav-link dropdown-toggle nav-user" data-toggle="dropdown" href="#" role="button"
                    aria-haspopup="false" aria-expanded="false">
                    <img src="@/../public/assets/images/users/user-1.jpg" alt="profile-user" class="rounded-circle" />
                    <span class="ml-1 nav-user-name hidden-sm">{{userProfile.email}} <i class="mdi mdi-chevron-down"></i> </span>
                </a>
                <div class="dropdown-menu dropdown-menu-right">
                    <a class="dropdown-item" href="/"><i class="dripicons-user text-muted mr-2"></i> Profile</a>
                    <a class="dropdown-item" href="/#/dashboard"><i class="dripicons-home text-muted mr-2"></i> Dashboard</a>
                    <a class="dropdown-item" href="/#/admin/users" v-if="hasAdminPageAccess(userProfile)">
                        <i class="dripicons-monitor text-muted mr-2"></i> Admin
                    </a>
                    <a class="dropdown-item" href="/#/admin/orgs" v-if="userProfile.is_staff || userProfile.is_superuser">
                        <i class="dripicons-suitcase text-muted mr-2"></i> Organizations
                    </a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item bg-light" @click="signOut" href="#"><i class="dripicons-exit text-muted mr-2"></i> Logout</a>
                </div>
            </li>
        </ul>
    </nav>
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
