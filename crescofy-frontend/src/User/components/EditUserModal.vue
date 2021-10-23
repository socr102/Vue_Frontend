<template>
<!-- Edit user modal window -->
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="editDialogLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="editDialogLabel">Edit account</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <UserForm
        v-on:form-change="onFormChange"
        :onSubmit="onSubmit"
        :isEditMode="true"
        :initData="userToEdit"
        :roles="getAvailableRoles('update')"
      />
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import UserForm from './UserForm';
import { UserRoleMixin } from '@/Core/mixins/UserRoleMixin';
import { UPDATE_USER }  from '@/Core/store/action-types';

export default {
  name: 'EditUser',
  mixins: [UserRoleMixin],
  components: {
    UserForm
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
    userToEdit: {
      required: true,
      type: Object,
    },
  },
  computed: {
    ...mapGetters('user', ['userProfile']),
    ...mapGetters('org', ['orgsList'])
  },

  methods: {
    ...mapActions('user', [UPDATE_USER]),

    onSubmit(values, actions) {
      let userToUpdate = this.getUser(values.role);
      userToUpdate.email = values.email;
      userToUpdate.id = this.userToEdit.id;
      if (this.isMerchantSelected()) {
        userToUpdate.organization = parseInt(values.organization);
      }

      if (this.formValues.isPasswordEdited && values.password)
        userToUpdate.password = values.password;

      this[UPDATE_USER]({userToUpdate, actions})
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('User successfully updated.', 'success', 3);
          actions.resetForm();
        })
        .catch(() => {})
    },

    onFormChange(form) {
      this.formValues = form;
    }
  },

  data() {
    return {
      formValues: {},
    }
  }
}
</script>