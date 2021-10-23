<template>
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="{{modalId}}" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" :id="modalId">{{header_text}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <Form @submit="onSubmit"
            :validation-schema="schema"
            v-slot="{ errors }"
            class="form-horizontal"
            action="#">
        <div class="modal-body">
            <div class="form-group" :class="{ 'has-error': errors.name }">
              <label for="name">Name</label>
              <Field as="input"
                     type="text"
                     class="form-control"
                     name="name"
                     placeholder="Enter Org Name"
                     v-model="formValues.name"/>
              <div class="form-control-feedback">{{errors.name}}</div>
            </div><!--end form-group-->

            <div class="form-group"  :class="{ 'has-error': errors.detail }">
              <Field as="input" type="hidden" class="form-control" name="detail"/>
              <div class="form-control-feedback">{{errors.detail}}</div>
            </div><!--end form-group-->
        </div>
        <div class="modal-footer">
          <button type="submit" class="btn btn-primary">{{btn_name}}</button>
          <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button>
        </div>
      </Form><!--end form-->
    </div>
  </div>
</div>
</template>

<script>
import { Field, Form } from 'vee-validate';
import * as yup from 'yup';
import { mapGetters, mapActions } from 'vuex';

import { UPDATE_ORG, CREATE_ORG }  from '@/Core/store/action-types';

export default {
  name: 'OrgModal',
  components: {
    Form,
    Field
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
    orgToEdit: {
      required: false,
      type: Object,
    },
    modalType: {
      required: true,
      type: Number,
    },
  },
  computed: {
    ...mapGetters('user', ['userProfile'])
  },
  watch: {
    orgToEdit: function(org) {
      this.formValues = {
        name: org.name
      }
    }
  },
  methods: {
    ...mapActions('org', [UPDATE_ORG, CREATE_ORG]),

    onSubmit(values, actions) {
      if (this.modalType == 1) this.updateOrg(values, actions);
      if (this.modalType == 2) this.createOrg(values, actions);
    },

    updateOrg(orgToUpdate, actions) {
      orgToUpdate.id = this.orgToEdit.id;
      this[UPDATE_ORG]({orgToUpdate, actions})
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('Organization successfully updated.', 'success', 3);
          actions.resetForm();
        })
        .catch(() => {})
    },

    createOrg(orgToCreate, actions) {
      this[CREATE_ORG]({orgToCreate, actions})
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('Organization successfully created.', 'success', 3);
          actions.resetForm();
        })
        .catch(() => {})
    },
  },

  beforeCreate() {
    if (this.modalType == 1) {
      // Edit mode
      this.btn_name = 'Edit';
      this.header_text = 'Edit organization';

    } else if (this.modalType == 2) {
      // Create mode
      this.btn_name = 'Create';
      this.header_text = 'Create new organization';
    }
  },

  data() {
    return {
      formValues: {},
      schema: yup.object().shape({
        name: yup.string()
          .min(6, 'Name must be at least 6 characters')
          .required('Please enter organization name'),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired()
      })
    }
  }
}
</script>