<template>
  <div>
      <FormModal :modalId="editModalId" :offerToEdit="editedResource" :modalType="1"/>
      <FormModal :modalId="createModalId" :modalType="2"/>
      <div :id='gridPanelId'></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import FormModal from './FormModal';
import { LIST_OFFERS, DELETE_OFFER } from '@/Core/store/action-types';
import StatusMixin from '@/Core/mixins/StatusMixin';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { controlField, onDeleteItem } from '@/Core/helpers/gridUtils';
import { RESOURCE_NAME } from '../offer.vars';
import '@/Core/helpers/DateRangeField';


export default {
  name: 'OfferGrid',
  components: { FormModal },
  mixins: [ StatusMixin, GlobalGridMixin ],
  computed: {
    ...mapGetters('offer', ["offersList"]),
    ...mapGetters('user', ["userProfile"])
  },
  methods: {
    ...mapActions('offer', [LIST_OFFERS, DELETE_OFFER]),

    getGridFields() {
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      return [
        { name: "name", type: "text", width: "auto",
          title: "Name", autosearch: true },
        { name: "details", type: "text", width: "auto",
          title: "Details", filtering: false },
        { name: "articles", type: "text", width: "auto",
          title: "Articles", filtering: false,
          itemTemplate: (articles) => {
            if (!articles) return '';
            return articles.map(article => {
              return window.$("<span>")
                .attr({class: 'rounded-pill badge larg-badge'})
                .text(article.name);
            })}
        },
        { name: "date", type: "daterange", width: "auto",
          title: "Date Range", autosearch: true
        },
        { type: "select", title: "Status", width: "auto", name: 'status',
          items: this.statusList, autosearch: true,
          itemTemplate: (val, item) => {
            return this.getStatusIcon(item);
          },
        },
        { name: "id", type: "number", visible: false, width: "auto" },
        controlField(showDetailsDialog, `Register new ${RESOURCE_NAME}`)
      ]
    },

    /**
     * Load offers from server and apply filters
     */
    loadOffers(filter) {
      let params = this.getStatusFilterProps(filter);
      if (filter.name) params.name = filter.name;

      if (filter.date) {
        params.start_date = filter.date.start_date;
        params.end_date = filter.date.end_date;
      }

      return this[LIST_OFFERS](params);
    }
  },
  mounted() {
    this.grid = window.$(`#${this.gridPanelId}`).jsGrid({
      height: "90%",
      width: "100%",
      autoload: true,
      paging: true,
      heading: true,
      filtering: true,
      editing: false,
      pageSize: 15,
      confirmDeleting: false,
      controller: {
        loadData: this.loadOffers
      },
      onItemDeleting: onDeleteItem(this.$alertify, this.$ability,
                                   this[DELETE_OFFER], RESOURCE_NAME),
      fields: this.getGridFields(),
      editItem: (item) => this.onUpdateItem(RESOURCE_NAME,
                                            window.$(`#${this.editModalId}`),
                                            item)
    });
  },
  watch: {
    offersList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.offersList);
      },
      deep: true
    }
  },
  data() {
    return {
      editedResource: {},
      statusList: ["ALL", "Pending", "Active", "Expired"],
      gridPanelId: "offersGrid",
      createModalId: "createDialog",
      editModalId: "editDialog"
    }
  }
}
</script>
