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
                     placeholder="Enter Offer Name"
                     v-model="formValues.name"/>
              <div class="form-control-feedback">{{errors.name}}</div>
            </div>
            <div class="form-group" :class="{ 'has-error': errors.details }">
              <label for="details">Offer Details</label>
              <Field as="input"
                     type="text"
                     class="form-control"
                     name="details"
                     placeholder="Enter Offer details"
                     v-model="formValues.details"/>
              <div class="form-control-feedback">{{errors.details}}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.start_date || errors.end_date }">
              <label for="date">Offer Date Range</label>
              <input type="text" ref="date" class="form-control"/>
              <div class="form-control-feedback">{{errors.start_date}}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.articles }">
              <label for="articles">Offer articles</label>
              <Field v-model="formValues.articles" name="articles">
                <Multiselect
                  v-model="formValues.articles"
                  mode="tags"
                  :minChars="3"
                  :resolveOnLoad="true"
                  :filterResults="false"
                  label="name"
                  valueProp="id"
                  :delay="0"
                  :searchable="true"
                  :options="fetchArticles"
                  placeholder="Select offer articles"
                  ref="article_select"
                />
              </Field>
              <div class="form-control-feedback">{{errors.articles}}</div>
            </div>
            <div class="form-group">
              <Field as="input" type="hidden" class="form-control"
                     name="start_date" v-model="formValues.start_date"/>
            </div>
            <div class="form-group">
              <Field as="input" type="hidden" class="form-control"
                     name="end_date" v-model="formValues.end_date"/>
            </div>
            <div class="form-group">
              <Field as="input" type="hidden" class="form-control" name="detail"/>
              <div class="form-control-feedback">{{errors.detail}}</div>
            </div>
        </div>
        <div class="modal-footer">
          <button type="submit" class="btn btn-primary">{{btn_name}}</button>
          <button type="button" class="btn btn-danger" data-dismiss="modal">Cancel</button>
        </div>
      </Form>
    </div>
  </div>
</div>
</template>

<script>
import { Field, Form } from 'vee-validate';
import * as yup from 'yup';
import Multiselect from '@vueform/multiselect'
import { mapGetters, mapActions } from 'vuex';

import { UPDATE_OFFER, CREATE_OFFER, LIST_ARTICLES }  from '@/Core/store/action-types';
import { DATE_FORMAT, DATE_REGEX } from '@/Core/helpers/utils';
import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';

export default {
  name: 'OfferModal',
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
    offerToEdit: {
      required: false,
      type: Object,
      default: function () {
        return {}
      }
    },
    modalType: {
      required: true,
      type: Number,
    },
  },
  computed: {
    ...mapGetters('article', ['articlesList'])
  },
  methods: {
    ...mapActions('offer', [UPDATE_OFFER, CREATE_OFFER]),
    ...mapActions('article', [LIST_ARTICLES]),

    onSubmit(values, actions) {
      if (this.modalType == 1) this.updateOffer(values, actions);
      if (this.modalType == 2) this.createOffer(values, actions);
    },

    updateOffer(obj, actions) {
      obj.id = this.offerToEdit.id;
      this[UPDATE_OFFER]({obj, actions})
        .then(() => {
          this.hideModal(actions);
          this.$alertify.notify('Offer successfully updated.', 'success', 3);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    createOffer(obj, actions) {
      this[CREATE_OFFER]({obj, actions})
        .then(() => {
          this.hideModal(actions);
          this.$alertify.notify('Offer successfully created.', 'success', 3);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    onDateChange(from_date, to_date) {
      this.formValues.start_date = from_date.format(DATE_FORMAT);
      this.formValues.end_date = to_date.format(DATE_FORMAT);

      this.setDateRange(this.formValues.start_date,
                        this.formValues.end_date);
    },

    setDateRange(start_date, end_date) {
      var dateRange = start_date && end_date ?
                      `${start_date} - ${end_date}` : ""
      this.datepicker.val(dateRange);
    },

    clearForm(actions) {
      actions.resetForm();
      this.formValues = {};
      this.$refs.article_select.clear();
      this.setDateRange();
    },

    hideModal(actions) {
      window.$(`#${this.modalId}`)
        .modal('hide')
        .on('hidden.bs.modal', () => {
          this.clearForm(actions);
        })
    },

    async fetchArticles(query) {
      if (!query && this.offerToEdit.articles)
        return this.offerToEdit.articles;
      if (query)
        return await this[LIST_ARTICLES]({params: {name: query}});
      return [];
    }
  },

  beforeCreate() {
    if (this.modalType == 1) {
      // Edit mode
      this.btn_name = 'Edit';
      this.header_text = 'Edit offer';

    } else if (this.modalType == 2) {
      // Create mode
      this.btn_name = 'Create';
      this.header_text = 'Create new offer';
    }
  },

  mounted() {
    this.datepicker = window.$(this.$refs.date);

    this.datepicker.daterangepicker({
      autoUpdateInput: false
    }, this.onDateChange);
  },

  watch: {
    offerToEdit: function (newOffer) {
      this.$refs.article_select.resolveOptions();
      this.formValues = Object.assign({}, newOffer);
      this.$nextTick(() => {
        this.formValues.articles = newOffer.articles.map(a => a.id);
      })

      this.setDateRange(newOffer.start_date, newOffer.end_date);
      if (newOffer.start_date && newOffer.end_date) {
        let start_date = window.moment(newOffer.start_date, DATE_FORMAT).toDate();
        let end_date = window.moment(newOffer.end_date, DATE_FORMAT).toDate();
        this.datepicker.data('daterangepicker').setStartDate(start_date);
        this.datepicker.data('daterangepicker').setEndDate(end_date);
      }
    }
  },

  data() {
    return { formValues: {} }
  },
  setup() {
    return {
      schema: yup.object().shape({
        name: yup.string()
          .min(6, 'Name must be at least 6 characters')
          .required('Please enter offer name'),
        details: yup.string()
          .min(6, 'Offer details must be at least 6 characters')
          .required('Please enter offer details'),
        articles: yup.array()
          .min(1)
          .required('Please select article to offer'),
        start_date: yup.string()
          .matches(DATE_REGEX, 'Please select valid date')
          .required('Please select offer date'),
        end_date: yup.string().matches(DATE_REGEX),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired()
      })
    }
  }
}
</script>

<style>
.has-error .multiselect-input {
  border-color: #ef4d56;
}
</style>
