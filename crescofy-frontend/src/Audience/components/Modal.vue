<template>
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="{{modalId}}" aria-hidden="true">
  <div class="modal-dialog modal-lg" role="document">
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

            <div class="card card-border">
              <h5 class="card-header bg-primary text-white mt-0">Member Filters</h5>
              <div class="card-body">
                <div class="form-group" :class="{ 'has-error': errors.sex }" >
                  <label for="sex">Sex</label>
                  <Field as="select" class="form-control" name="sex" v-model="formValues.sex">
                  <option v-for="sex in genderTypes" v-bind:key="sex">
                      {{sex}}
                  </option>
                  </Field>
                  <div class="form-control-feedback">{{errors.sex}}</div>
                </div>

                <div class="form-group" :class="{ 'has-error': errors.articles }">
                  <label for="articles">Audience Age</label>
                  <Field v-model="formValues.age" name="age">
                    <Slider v-model="ageSlider"
                            @change="ageChanged"/>
                  </Field>
                  <div class="form-control-feedback">{{errors.age}}</div>
                </div>

                <div class="form-group" :class="{ 'has-error': errors.articles }">
                  <label for="articles">Article Preferences</label>
                  <Field v-model="formValues.articles" name="articles">
                    <Multiselect
                      v-model="formValues.articles"
                      mode="tags"
                      :minChars="3"
                      :resolveOnLoad="false"
                      :filterResults="false"
                      label="name"
                      valueProp="id"
                      :delay="0"
                      :searchable="true"
                      :options="fetchArticles"
                      placeholder="Select article"
                      ref="article_select"
                    />
                  </Field>

                  <div class="form-control-feedback">{{errors.articles}}</div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="members">Select members manually</label>
              <Field as="input" type="hidden" class="form-control"
                     name="members" v-model="formValues.members"/>
              <div class="form-control-feedback">{{errors.members}}</div>
            </div>

            <div class="form-group">
              <MembersGrid
                :preSelectedMemberIds="filteredMembers"
                v-on:update="formValues.members = $event" />
            </div>

            <div class="form-group">
              <Field as="input" type="hidden" class="form-control" name="detail"/>
              <div class="form-control-feedback">{{errors.detail}}</div>
              <strong>Selected members: {{formValues.members.length}}</strong>
            </div>
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
import Multiselect from '@vueform/multiselect';
import Slider from '@vueform/slider';
import { mapGetters, mapActions } from 'vuex';

import {UPDATE_AUDIENCE,
        CREATE_AUDIENCE,
        LIST_MEMBERS,
        LIST_ARTICLES }  from '@/Core/store/action-types';
import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';
import MembersGrid from '@/Members/components/SelectorGrid';

const DEFAULT_AGE_SLIDER = [0, 100];

export default {
  name: 'AudienceModal',
  components: {
    Form,
    Field,
    Multiselect,
    Slider,
    MembersGrid
  },
  props: {
    modalId: {
      required: true,
      type: String,
    },
    audienceToEdit: {
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
    ...mapGetters('member', ['membersList']),
    ...mapGetters('audience', ['audienceList']),
    ...mapGetters('article', ['articlesList']),

    filter() {
      return {
        sex: this.formValues.sex != 'All' ? this.formValues.sex: undefined,
        age_min: this.formValues.age_min,
        age_max: this.formValues.age_max,
        prefs: this.formValues.articles
      }
    }
  },
  methods: {
    ...mapActions('audience', [UPDATE_AUDIENCE, CREATE_AUDIENCE]),
    ...mapActions('member', [LIST_MEMBERS]),
    ...mapActions('article', [LIST_ARTICLES]),

    onSubmit(values, actions) {
      if (!this.formValues.members.length) {
        actions.setFieldError('members', 'Please select at least one member');
        return;
      }
      if (this.modalType == 1) this.updateAudience(values, actions);
      if (this.modalType == 2) this.createAudience(values, actions);
    },

    updateAudience(obj, actions) {
      obj.id = this.audienceToEdit.id;
      this[UPDATE_AUDIENCE](obj)
        .then(() => {
          this.hideModal();
          this.$alertify.notify('Audience successfully updated.', 'success', 3);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    createAudience(obj, actions) {
      this[CREATE_AUDIENCE](obj)
        .then(() => {
          this.hideModal();
          this.$alertify.notify('Audience successfully created.', 'success', 3);
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    clearForm() {
      this.filteredMembers = [];
      if (!this.audienceToEdit) this.formValues = this.initForm();
      this.$refs.article_select.clear();
    },

    hideModal() {
      window.$(`#${this.modalId}`).modal('hide');
    },

    ageChanged(value) {
      this.formValues.age_min = value[0];
      this.formValues.age_max = value[1];
    },

    async searchMembers(query) {
      let data = await this[LIST_MEMBERS]({params: {q: query}});
      return data;
    },

    initForm() {
      return { sex: 'All', members: [] };
    },

    filterWatcher(params) {
      this[LIST_MEMBERS]({params}).then(data => {
        this.filteredMembers = data.map(m => m.id);
        this.formValues.members = this.filteredMembers;
      })
    },
    async fetchArticles(query) {
      return await this[LIST_ARTICLES]({params: {name: query}});
    }
  },

  beforeCreate() {
    if (this.modalType == 1) {
      // Edit mode
      this.btn_name = 'Edit';
      this.header_text = 'Edit audience';

    } else if (this.modalType == 2) {
      // Create mode
      this.btn_name = 'Create';
      this.header_text = 'Create new audience';
    }
  },

  mounted() {
    window.$(`#${this.modalId}`)
      .on('hidden.bs.modal', () => {
        this.unwatch();
        this.clearForm();
      })
      .on('show.bs.modal', () => {
        this.ageSlider = [...DEFAULT_AGE_SLIDER];
        this.$nextTick(() => {
          this.unwatch = this.$watch('filter', this.filterWatcher);
        })
      })
  },

  watch: {
    audienceToEdit(newObj) {
      this.formValues = Object.assign(this.formValues, newObj);
      this.filteredMembers = this.formValues.members;
    }
  },

  data() {
    return {
      formValues: this.initForm(),
      filteredMembers: [],
      ageSlider: [...DEFAULT_AGE_SLIDER],
    }
  },
  setup() {
    let genderTypes = ["All", "Female", "Male"];
    return {
      genderTypes: genderTypes,
      schema: yup.object().shape({
        name: yup.string()
          .min(6, 'Name must be at least 6 characters')
          .required('Please enter audience name'),
        members: yup.array().notRequired(),
        age: yup.array().notRequired(),
        articles: yup.array().notRequired(),
        sex: yup.string()
          .oneOf(genderTypes)
          .notRequired(),
        preferences: yup.array().notRequired(),
        detail: yup.string() // use it for backend errors
          .nullable()
          .notRequired()
      })
    }
  }
}
</script>

<style src="@vueform/slider/themes/default.css"></style>

<style>
  .slider-connects div.slider-connect {
    background: #7680ff;
  }

  .slider-tooltip {
    font-size: 10px;
    background: #7680ff;
    border-color: #7680ff;
  }
</style>
