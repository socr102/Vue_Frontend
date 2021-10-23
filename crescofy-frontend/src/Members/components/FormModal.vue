<template>
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" :aria-labelledby="modalId" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" :id="modalId">{{header_text}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors }" class="form-horizontal" action="#">
        <div class="modal-body">
          <div class="form-group" :class="{ 'has-error': errors.name }">
            <label for="name">Name</label>
            <Field as="input" type="text" class="form-control" name="name" placeholder="Enter Name" v-model="formValues.name"/>
            <div class="form-control-feedback">{{errors.name}}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': errors.email }">
            <label for="email">Email</label>
            <Field as="input" type="text" class="form-control" name="email" placeholder="Enter Email" v-model="formValues.email"/>
            <div class="form-control-feedback">{{errors.email}}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': errors.phone }">
            <label for="name">Phone</label>
            <Field as="input" type="text" class="form-control" name="phone" placeholder="Enter Phone" v-model="formValues.phone"/>
            <div class="form-control-feedback">{{errors.phone}}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': errors.sex }">
            <label for="name">Sex</label>
            <Field as="select" class="form-control" name="sex" v-model="formValues.sex">
              <option v-for="sex in sexChoices" v-bind:key="sex" v-bind:value="sex">
                {{sex}}
              </option>
            </Field>
            <div class="form-control-feedback">{{errors.sex}}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': errors.external_id }">
            <label for="name">External ID</label>
            <Field as="input" type="text" class="form-control" name="external_id" placeholder="Enter External ID" v-model="formValues.external_id"/>
            <div class="form-control-feedback">{{errors.external_id}}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': errors.birth_date}">
            <label for="date">Birth Date</label>
            <input type="text" ref="date" class="form-control"/>
            <div class="form-control-feedback">{{errors.birth_date}}</div>
          </div>

          <div class="form-group">
            <Field as="input" type="hidden" class="form-control" name="birth_date" v-model="formValues.birth_date"/>
          </div>

          <div class="form-group"  :class="{ 'has-error': errors.detail }">
            <Field as="input" type="hidden" class="form-control" name="detail"/>
            <div class="form-control-feedback">{{errors.detail}}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="submit" class="btn btn-primary">{{btn_name}}</button>
          <button type="button" class="btn btn-danger" data-dismiss="modal" v-on:click="clearForm()">Cancel</button>
        </div>
      </Form>
    </div>
  </div>
</div>
</template>

<script>
import { Field, Form } from 'vee-validate';
import * as yup from 'yup';
import { mapGetters, mapActions } from 'vuex';

import { UPDATE_MEMBER, CREATE_MEMBER }  from '@/Core/store/action-types';
import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';
import { PHONE_REGEX, DATE_REGEX, DATE_FORMAT } from '@/Core/helpers/utils';
import { RESOURCE_NAME } from '../member.vars';

export default {
  name: 'MemberModal',
  components: {
    Form,
    Field
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
    memberToEdit: {
      required: false,
      type: Object,
      default: function () {
        return undefined;
      }
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
    memberToEdit: function(obj) {
      this.originalResource = obj;
      this.formValues = this.initForm();
    }
  },
  methods: {
    ...mapActions('member', [UPDATE_MEMBER, CREATE_MEMBER]),

    onSubmit(values, actions) {
      if (this.modalType == 1) this.updateMember(values, actions);
      if (this.modalType == 2) this.createMember(values, actions);
    },

    updateMember(obj, actions) {
      obj.id = this.memberToEdit.id;
      this[UPDATE_MEMBER](obj)
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify(`${RESOURCE_NAME} successfully updated.`, 'success', 3);
          this.clearForm(actions);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    createMember(obj, actions) {
      this[CREATE_MEMBER](obj)
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify(`${RESOURCE_NAME} successfully created.`, 'success', 3);
          this.clearForm(actions);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    clearForm(actions) {
      this.formValues = this.initForm();
      if (actions) actions.resetForm();
    },

    initForm() {
      if (this.originalResource) {
        this.setDatepicker(this.originalResource.birth_date);
        return Object.assign({}, this.originalResource);
      }

      return {
        name: '',
        email: '',
        phone: '',
        sex: null,
        external_id: '',
        birth_date: null
      }
    },

    onDateChange(start) {
      this.formValues.birth_date = start.format(DATE_FORMAT);
      this.setDatepicker(this.formValues.birth_date);
    },

    setDatepicker(date) {
      this.datepicker.val(date);
    },
  },

  mounted() {
    this.datepicker = window.$(this.$refs.date);
    this.datepicker.daterangepicker({
      singleDatePicker: true,
      showDropdowns: true,
      autoUpdateInput: false
    }, this.onDateChange);
  },

  beforeCreate() {
    if (this.modalType == 1) {
      // Edit mode
      this.btn_name = 'Edit';
      this.header_text = `Edit ${RESOURCE_NAME}`;

    } else if (this.modalType == 2) {
      // Create mode
      this.btn_name = 'Create';
      this.header_text = `Create new ${RESOURCE_NAME}`;
    }
  },

  data() {
    var sexChoices = ["Female", "Male"];
    return {
      resourceName: RESOURCE_NAME,
      sexChoices: sexChoices,
      formValues: this.initForm(),
      schema: yup.object().shape({
        name: yup.string()
          .min(6, 'Name must be at least 6 characters')
          .required(`Please enter ${RESOURCE_NAME.toLowerCase()} name`),
        email: yup.string().required('Email is required')
                           .email('Email is invalid'),
        phone: yup.string()
          .matches(PHONE_REGEX, 'Phone number is not valid')
          .required('Phone is required'),
        external_id: yup.string()
          .min(6, 'External ID must be at least 6 characters')
          .required(`Please enter ${RESOURCE_NAME.toLowerCase()} name`),
        birth_date: yup.string()
          .matches(DATE_REGEX, 'Please select valid date')
          .nullable(),
        sex: yup.string()
          .oneOf(sexChoices)
          .required('Please indicate sex'),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired(),
      })
    }
  }
}
</script>
