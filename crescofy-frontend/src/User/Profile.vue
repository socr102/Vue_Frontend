<template>
  <div class="page-wrapper">
    <!-- Page Content-->
    <div class="page-content-tab">
      <div class="container">
          <!-- Page-Title -->
          <div class="row">
              <div class="col-sm-12">
                  <div class="page-title-box">
                      <h4 class="page-title">Profile</h4>
                  </div><!--end page-title-box-->
              </div><!--end col-->
          </div>
          <div class="card">
            <div class="card-body">
              <div class="row met-profile">
                <div class="col-lg-4 align-self-center mb-3 mb-lg-0">
                      <div class="met-profile-main">
                          <div class="met-profile-main-pic">
                              <img src="../../public/assets/images/users/user-4.jpg" alt="" height="100" class="rounded-circle">
                              <span class="fro-profile_main-pic-change">
                                  <i class="fas fa-camera"></i>
                              </span>
                          </div>
                          <div class="met-profile_user-detail">
                              <h5 class="met-user-name">{{userProfile.email}}</h5>
                              <p class="mb-0 met-user-name-post">{{getUserRole(userProfile)}}</p>
                          </div>
                      </div>
                  </div><!--end col-->
                </div><!--end row-->
              </div>
            </div>

            <div class="card">
              <div class="card-body col-lg-6">
                <h4 class="mt-0 header-title">Reset password</h4>
                <div class="general-label">
                  <Form @submit="onSubmit" :validation-schema="schema"
                    v-slot="{ errors }" action="#">

                    <div class="form-group row" :class="{ 'has-error': errors.old_password }">
                      <label for="old_password" class="col-sm-4 col-form-label">Current Password</label>
                      <div class="col-sm-8">
                        <Field as="input" type="password" class="form-control" name="old_password" placeholder="Enter current password"/>
                      <div class="form-control-feedback">{{errors.old_password}}</div>
                      </div>

                    </div><!--end form-group-->

                    <div class="form-group row" :class="{ 'has-error': errors.new_password }">
                      <label for="new_password" class="col-sm-4 col-form-label">New Password</label>
                      <div class="col-sm-8">
                        <Field as="input" type="password" class="form-control" name="new_password" placeholder="Enter new password"/>
                      <div class="form-control-feedback">{{errors.new_password}}</div>
                      </div>
                    </div><!--end form-group-->

                    <div class="form-group row" :class="{ 'has-error': errors.confirm_password }">
                      <label for="confirm_password" class="col-sm-4 col-form-label">Confirm Password</label>

                      <div class="col-sm-8">
                        <Field as="input" type="password" class="form-control" name="confirm_password" placeholder="Enter Confirm Password"/>
                      <div class="form-control-feedback">{{errors.confirm_password}}</div>
                      </div>
                    </div><!--end form-group-->

                    <div class="form-group row"  :class="{ 'has-error': errors.detail }">
                      <div class="col-sm-8 ml-auto">
                        <Field as="input" type="hidden" class="form-control" name="detail"/>
                        <div class="form-control-feedback">{{errors.detail}}</div>
                      </div>
                    </div><!--end form-group-->

                    <div class="row">

                      <div class="col-sm-8 ml-auto">
                        <button type="submit" class="btn btn-sm btn-primary">Reset Password</button>
                      </div><!--end col-->
                    </div> <!--end form-group-->
                  </Form><!--end form-->
                </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Field, Form } from 'vee-validate';
import * as yup from 'yup';
import { mapActions, mapGetters } from 'vuex';

import { CHANGE_OWN_PASSWORD } from '@/Core/store/action-types';
import { UserRoleMixin } from '@/Core/mixins/UserRoleMixin';

export default {
  name: 'Profile',
  components: {
    Form,
    Field
  },
  mixins: [UserRoleMixin],
  methods: {
    ...mapActions('user', [CHANGE_OWN_PASSWORD]),
    onSubmit(values, actions) {
      let form = {values, actions, userId: this.userProfile.id};
      this[CHANGE_OWN_PASSWORD](form)
        .then(() => {
          this.$alertify.notify('Password successfully updated.',
                                'success',
                                 3);
          actions.resetForm();
        }).catch(() => {}) //stay on a page
    }
  },
  computed: {
    ...mapGetters('user', {userProfile: 'userProfile'})
  },
  setup() {
    const schema = yup.object().shape({
      old_password: yup.string()
        .min(6, 'Password must be at least 6 characters')
        .required('Current password is required'),
      new_password: yup.string()
        .min(6, 'Password must be at least 6 characters')
        .required('New password is required'),
      confirm_password: yup.string()
        .oneOf([yup.ref('new_password'), null], 'Passwords must match')
        .required('Confirm Password is required'),
      detail: yup.string() // use it for backend errors
        .nullable()
        .notRequired()
    });

    return {
        schema
    };
  }
}
</script>
