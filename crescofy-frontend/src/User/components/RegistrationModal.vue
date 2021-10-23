<template>
<!-- Register modal window -->
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="createDialogLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="createDialogLabel">Create new account</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <UserForm
        :onSubmit="onSubmit"
        :isEditMode="false"
        :roles="getAvailableRoles('create')"
      />
    </div>
  </div>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { REGISTER }  from '@/Core/store/action-types';
import { UserRoleMixin } from '@/Core/mixins/UserRoleMixin';
import UserForm from './UserForm';

export default {
  name: 'Registration',
  mixins: [UserRoleMixin],
  components: {
    UserForm
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
  },
  computed: {
    ...mapGetters('user', ['userProfile']),
    ...mapGetters('org', ['orgsList'])
  },
  methods: {
    ...mapActions('user', [REGISTER]),

    onSubmit(values, actions) {
      let userToCreate = this.getUser(values.role);
      userToCreate.email = values.email;
      userToCreate.password = values.password;
      userToCreate.organization = parseInt(values.organization);

      this[REGISTER]({userToCreate, actions})
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('User successfully created.', 'success', 3);
          actions.resetForm();
        })
        .catch(() => {})
    }
  },

  data() {
    return {};
  }
}
</script>