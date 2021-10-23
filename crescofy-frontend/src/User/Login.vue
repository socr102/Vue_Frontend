<template>
<!-- Log In page -->
<div class="container">
    <div class="row vh-100 d-flex justify-content-center">
        <div class="col-12 align-self-center">
            <div class="">
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-5 mx-auto">
                            <div class="card">
                                <div class="card-body">
                                    <div class="media mb-3">
                                        <a href="../analytics/analytics-index.html" class="logo logo-admin">
                                            <img src="../../public/assets/images/logo-sm.png" height="40" alt="logo" class="auth-logo">
                                        </a>
                                    </div>
                                    <Form @submit="onSubmit" :validation-schema="schema"
                                        v-slot="{ errors }" class="form-horizontal auth-form my-4" action="index.html">

                                        <div class="form-group" :class="{ 'has-error': errors.email }">
                                          <label for="email">Email</label>
                                          <Field as="input" type="email" class="form-control form-control-danger" name="email" placeholder="Enter Email"/>
                                          <div class="form-control-feedback">{{errors.email}}</div>
                                        </div><!--end form-group-->

                                        <div class="form-group" :class="{ 'has-error': errors.password }">
                                          <label for="password">Password</label>
                                          <Field as="input" type="password" class="form-control" name="password" placeholder="Enter password"/>
                                          <div class="form-control-feedback">{{errors.password}}</div>
                                        </div><!--end form-group-->

                                        <div class="form-group"  :class="{ 'has-error': errors.detail }">
                                          <Field as="input" type="hidden" class="form-control" name="detail"/>
                                          <div class="form-control-feedback">{{errors.detail}}</div>
                                        </div><!--end form-group-->

                                        <div class="form-group mb-0 row">
                                          <div class="col-12 mt-2">
                                            <button class="btn btn-primary btn-block waves-effect waves-light" type="submit"> Log In <i class="fas fa-sign-in-alt ml-1"></i></button>
                                          </div><!--end col-->
                                        </div> <!--end form-group-->
                                    </Form><!--end form-->
                                </div>
                            </div>
                        </div><!--end col-->
                    </div><!--end row-->
                </div><!--end card-body-->
            </div><!--end card-->
        </div><!--end col-->
    </div><!--end row-->
</div><!--end container-->
<!-- End Log In page -->
</template>

<script>
import { Field, Form } from 'vee-validate';
import * as yup from 'yup';
import { mapActions } from 'vuex';

import { LOGIN } from '@/Core/store/action-types';
import {UserRoleMixin} from '@/Core/mixins/UserRoleMixin';

export default {
  name: 'Login',
  components: {
    Form,
    Field
  },
  mixins: [UserRoleMixin],
  methods: {
    ...mapActions('user', [LOGIN]),
    onSubmit(values, actions) {
      this[LOGIN]({values, actions, ability: this.$ability})
        .then(() => {
          // got to the homepage
          this.$router.push('/');
        }).catch(() => {}) //stay on a page
    }
  },
  data() {
    const schema = yup.object().shape({
      email: this.emailValidator(),
      password: yup.string()
        .min(6, 'Password must be at least 6 characters')
        .required('Password is required'),
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
