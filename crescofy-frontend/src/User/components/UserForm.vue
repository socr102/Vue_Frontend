<template>
<Form @submit="onSubmit"
        :validation-schema="schema"
        v-slot="{ errors }"
        class="form-horizontal"
        action="#">
    <div class="modal-body">
        <div class="form-group" :class="{ 'has-error': errors.email }">
            <label for="email">Email</label>
            <Field as="input"
                    type="email"
                    class="form-control"
                    name="email"
                    placeholder="Enter Email"
                    v-model="formValues.email"/>
            <div class="form-control-feedback">{{errors.email}}</div>
        </div><!--end form-group-->

        <div class="form-group" :class="{ 'has-error': errors.role }" >
            <label for="role">Role</label>
            <Field as="select" class="form-control" name="role" v-model="formValues.role">
            <option v-for="role in roles" v-bind:key="role">
                {{role}}
            </option>
            </Field>
            <div class="form-control-feedback">{{errors.role}}</div>
        </div><!--end form-group-->

        <div class="form-group" :class="{ 'has-error': errors.organization }" v-if="isMerchantSelected()">
            <label for="organization">Organization</label>
            <Field as="select" class="form-control" name="organization" v-model="formValues.organization">
            <option v-for="org in orgsList" v-bind:key="org.id" v-bind:value="org.id">
                {{org.name}}
            </option>
            </Field>
            <div class="form-control-feedback">{{errors.organization}}</div>
        </div><!--end form-group-->

        <div class="form-group form-check" v-if="isEditMode">
            <input type="checkbox" class="form-check-input" v-model="formValues.isPasswordEdited">
            <label for="checkbox" class="form-check-label">Edit password</label>
        </div><!--end form-group-->

        <div class="form-group" :class="{ 'has-error': errors.password }" v-if="formValues.isPasswordEdited">
            <label for="password">Password</label>
            <Field as="input" type="password" class="form-control" name="password" placeholder="Enter password"/>
            <div class="form-control-feedback">{{errors.password}}</div>
        </div><!--end form-group-->

        <div class="form-group" :class="{ 'has-error': errors.confirmPassword }" v-if="formValues.isPasswordEdited">
            <label for="confirmPassword">Confirm Password</label>
            <Field as="input" type="password" class="form-control" name="confirmPassword" placeholder="Enter Confirm Password"/>
            <div class="form-control-feedback">{{errors.confirmPassword}}</div>
        </div><!--end form-group-->

        <div class="form-group"  :class="{ 'has-error': errors.detail }">
            <Field as="input" type="hidden" class="form-control" name="detail"/>
            <div class="form-control-feedback">{{errors.detail}}</div>
        </div><!--end form-group-->
    </div>
    <div class="modal-footer">
        <button type="submit" class="btn btn-primary">{{isEditMode ? 'Edit': 'Create' }}</button>
        <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button>
    </div>
</Form><!--end form-->
</template>

<script>
import { Field, Form } from 'vee-validate';
import { mapGetters } from 'vuex';
import * as yup from 'yup';

import {UserRoleMixin} from '@/Core/mixins/UserRoleMixin';

export default {
  name: 'UserForm',
  mixins: [UserRoleMixin],
  components: {
    Form,
    Field
  },
  props: {
    isEditMode: {
      required: false,
      default: false,
    },
    onSubmit: {
      required: true
    },
    roles: {
      required: true,
      type: Array
    },
    initData: {
      required: false
    }
  },
  emits: ['form-change'],
  computed: {
    ...mapGetters('org', ['orgsList'])
  },

  watch: {
    formValues: {
      handler: function(newForm) {
        this.$emit('form-change', newForm);
      },
      deep: true
    },
    initData: function(newUser) {
      this.formValues = {
        email: newUser.email,
        role: this.getUserRole(newUser),
        organization: newUser.organization
      }
    }
  },

  data() {
    return {
      formValues: {
        isPasswordEdited: this.isEditMode ? false: true,
        role: this.roles ? this.roles[0]: null
      },
      schema: yup.object().shape({
        email: this.emailValidator(),
        organization: this.orgValidator(),
        role: this.roleValidator(),
        password: yup.lazy(() => {
          if (this.formValues.isPasswordEdited) {
            return yup.string()
              .min(6, 'Password must be at least 6 characters')
              .required('Password is required')
          }
          return yup.string().notRequired();
        }),
        confirmPassword: yup.string()
          .oneOf([yup.ref('password'), null], 'Passwords must match')
          .required('Confirm Password is required'),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired()
      })
    }
  },
}
</script>
