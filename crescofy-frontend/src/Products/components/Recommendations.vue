<template>
<div>
  <div class="row">
    <div class="col-lg-12">
        <div class="card report-card">
            <div class="card-body text-center">
                <Multiselect
                  ref="multiselect"
                  v-model="value"
                  mode="tags"
                  label="name"
                  valueProp="id"
                  :minChars="3"
                  :resolveOnLoad="true"
                  :filterResults="false"
                  :delay="0"
                  :searchable="true"
                  :options="fetch"
                  :placeholder="selectPlaceholder"
                />
            </div>
            <button v-on:click="search" class="btn btn-outline-primary" type="button">Search</button>
        </div>
    </div>
  </div>

  <div class="row">
    <div class="col-lg-12">
        <div class="card report-card">
            <div :id="gridId"></div>
        </div>
    </div>
  </div>

</div>
</template>

<script>
import Multiselect from '@vueform/multiselect'
import * as yup from 'yup';

export default {
  name: 'Recommendations',
  components: { Multiselect },
  mixins: [],
  props: {
    fetchRecords: {
      required: true,
      type: Function,
    },
    initOptions: {
      required: false,
      default: () => [],
      type: Array,
    },
    selectPlaceholder: {
      required: true,
      type: String,
    },
    gridFields: {
      required: true,
      type: Array
    },
    endpoint: {
      required: true,
      type: Function
    },
    modelValue: {}
  },
  emits: ['update:modelValue', 'search'],
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    }
  },
  methods: {
    async fetch(query) {
      if (query) {
        var searchResult = await this.fetchRecords({params: {name: query},
                                                    persist: false});
        if (searchResult.length > 0) return searchResult;
      }

      return this.initOptions;
    },

    async search() {
      this.schema
        .validate({
          items: this.value,
        })
        .then(() => {
          this.endpoint(this.modelValue).then(recs => {
            this.recommendations = recs;
            this.grid.jsGrid("option", "data", this.recommendations);
            this.$emit('search', this.value);
          });

        })
        .catch((err) => {
          this.$alertify.notify(err.message, 'error', 3);
        });
    }
  },
  mounted() {
    this.grid = window.$(`#${this.gridId}`).jsGrid({
      height: "90%",
      width: "100%",
      autoload: true,
      paging: true,
      pageSize: 15,
      fields: this.gridFields,
      data: this.recommendations,
    });
  },

  watch: {
    initOptions: {
      handler: function() {
        this.$refs.multiselect.refreshOptions();
      },
      deep: true
    }
  },

  data() {
    return {
      gridId: 'recGrid',
      recommendations: [],
      schema: yup.object().shape({
        items: yup.array()
          .min(2)
          .max(10)
          .required('Please select items to search'),
      })
    }
  }
}
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

<style>
.multiselect-tag {
  background: #7680ff;
}
</style>