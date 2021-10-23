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
                     placeholder="Enter Audience Name"
                     v-model="formValues.name"/>
              <div class="form-control-feedback">{{errors.name}}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.offer }">
              <label for="offer">Offer</label>
              <Field v-model="formValues.offer" name="offer">
                <Multiselect
                  :id="modalId+'-offer'"
                  v-if="offersList"
                  valueProp="id"
                  label="name"
                  trackBy="name"
                  v-model="formValues.offer"
                  :options="offersList"
                />
              </Field>
              <div class="form-control-feedback">{{errors.offer}}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.audience }">
              <label for="audience">Audience</label>
              <Field v-model="formValues.audience" name="audience">
                <Multiselect
                  v-if="audienceList"
                  :id="modalId+'-audience'"
                  valueProp="id"
                  label="name"
                  trackBy="name"
                  v-model="formValues.audience"
                  :options="audienceList"
                />
              </Field>
              <div class="form-control-feedback">{{errors.audience}}</div>
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
import Multiselect from '@vueform/multiselect';

import { UPDATE_CAMPAIGN, CREATE_CAMPAIGN,
         LIST_OFFERS, LIST_AUDIENCE }  from '@/Core/store/action-types';
import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';

export default {
  name: 'CampaignModal',
  components: {
    Form,
    Field,
    Multiselect
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
    campaignToEdit: {
      required: false,
      type: Object,
    },
    modalType: {
      required: true,
      type: Number,
    },
  },
  computed: {
    ...mapGetters('user', ['userProfile']),
    ...mapGetters('offer', ['offersList']),
    ...mapGetters('audience', ['audienceList'])
  },
  watch: {
    campaignToEdit: function(obj) {
      this.originalResource = {
        name: obj.name,
        offer: obj.offer.id,
        audience: obj.audience.id
      };
      this.formValues = Object.assign({}, this.originalResource);
    }
  },
  methods: {
    ...mapActions('campaign', [UPDATE_CAMPAIGN, CREATE_CAMPAIGN]),
    ...mapActions('offer', [LIST_OFFERS]),
    ...mapActions('audience', [LIST_AUDIENCE]),

    onSubmit(values, actions) {
      if (this.modalType == 1) this.updateCampaign(values, actions);
      if (this.modalType == 2) this.createCampaign(values, actions);
    },

    updateCampaign(obj, actions) {
      obj.id = this.campaignToEdit.id;
      this[UPDATE_CAMPAIGN](obj)
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('Campaign successfully updated.', 'success', 3);
          this.clearForm(actions);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    createCampaign(obj, actions) {
      this[CREATE_CAMPAIGN](obj)
        .then(() => {
          window.$(`#${this.modalId}`).modal('hide');
          this.$alertify.notify('Campaign successfully created.', 'success', 3);
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
        return Object.assign({}, this.originalResource);
      }

      return {
        name: '',
        offer: null,
        audience: null
      }
    }
  },

  beforeCreate() {
    if (this.modalType == 1) {
      // Edit mode
      this.btn_name = 'Edit';
      this.header_text = 'Edit campaign';

    } else if (this.modalType == 2) {
      // Create mode
      this.btn_name = 'Create';
      this.header_text = 'Create new campaign';
    }
  },

  mounted() {
    this[LIST_OFFERS]();
    this[LIST_AUDIENCE]();
  },
  data() {
    let offerErr = 'Offer is required';
    let audienceErr = 'Audience is required';
    return {
      formValues: this.initForm(),
      schema: yup.object().shape({
        name: yup.string()
          .min(6, 'Name must be at least 6 characters')
          .required('Please enter campaign name'),
        offer: yup.lazy(() => {
          return yup.number()
            .oneOf(this.offersList.map(o => o.id), offerErr)
            .required(offerErr)
        }),
        audience: yup.lazy(() => {
          return yup.number()
            .oneOf(this.audienceList.map(a => a.id), audienceErr)
            .required(audienceErr)
        }),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired(),
      })
    }
  }
}
</script>
