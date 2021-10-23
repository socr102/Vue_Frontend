<template>
  <div>
      <FormModal :modalId="editModalId" :campaignToEdit="editedResource" :modalType="1"/>
      <FormModal :modalId="createModalId" :modalType="2"/>
      <Stats :modalId="statsModalId" :metadata="editedResource.metadata"/>
      <div :id='gridPanelId'></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { subject } from '@casl/ability';

import { LIST_CAMPAIGNS, DELETE_CAMPAIGN, DUPLICATE_CAMPAIGN } from '@/Core/store/action-types';
import StatusMixin from '@/Core/mixins/StatusMixin';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { onDeleteItem, controlField } from '@/Core/helpers/gridUtils';
import FormModal from './FormModal';
import Stats from './Stats';
import { RESOURCE_NAME } from '../campaign.vars';

export default {
  name: 'CampaignGrid',
  components: { FormModal, Stats },
  mixins: [ StatusMixin, GlobalGridMixin ],
  computed: {
    ...mapGetters('campaign', ["campaignsList"]),
    ...mapGetters('user', ["userProfile"])
  },
  methods: {
    ...mapActions('campaign', [LIST_CAMPAIGNS, DELETE_CAMPAIGN, DUPLICATE_CAMPAIGN]),

    getDuplciateBtn(item) {
      return window.$("<input>").attr({
        class: 'jsgrid-button jsgrid-insert-mode-button',
        type: 'button'
      })
        .click((e) => {
          this.onDuplicate(item);
          e.stopPropagation();
        });
    },

    getDetailsBtn(item) {
      return window.$("<input>").attr({
        class: 'jsgrid-button jsgrid-search-button',
        type: 'button'
      })
        .click((e) => {
          this.editedResource = item;
          window.$(`#${this.statsModalId}`).modal('toggle');
          e.stopPropagation();
        });
    },

    getGridFields() {
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      let vueContext = this;
      var control = controlField(showDetailsDialog,
                                 `Register new ${RESOURCE_NAME}`);
      control.itemTemplate = function() {
        var $result = window.jsGrid.fields.control.prototype
                            .itemTemplate.apply(this, arguments);

        let $duplicateBtn = vueContext.getDuplciateBtn(arguments[1]);
        let $detailsBtn = vueContext.getDetailsBtn(arguments[1]);
        return $result.add($duplicateBtn).add($detailsBtn);
      }

      return [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Campaign name", autosearch: true },
        { name: "offer.name", type: "number", width: "auto", title: "Offer", filtering: false},
        { name: "audience.name", type: "number", width: "auto", title: "Audience", filtering: false},
        { type: "select", title: "Status", width: "auto", name: 'status',
          items: this.statusList, autosearch: true,
          itemTemplate: (val, item) => {
            return this.getStatusIcon(item);
          },
        },
        { name: "id", type: "number", visible: false, width: "auto" },
        control
      ]
    },

    onDuplicate(item) {
      let hasPermission = this.$ability.can('duplicate',
                                            subject(RESOURCE_NAME, item));
      if (!hasPermission) {
        this.$alertify.notify('Action Forbidden!', 'error', 3);
      } else {
        let confirmMsg = `This action will duplicate ${item.name} ${RESOURCE_NAME}. Are you sure?`;
        this.$alertify.confirm(
          'Please Confirm Your Action',
          confirmMsg,
          () => {
            this[DUPLICATE_CAMPAIGN](item.id).then(() =>
              this.$alertify.notify('Campaign successfully duplicated.',
                                    'success',
                                    3));
          },
          () => {}
        );
      }
    },

    /**
     * Load campaigns from server and apply filters
     */
    loadCampaigns(filter) {
      let params = this.getStatusFilterProps(filter);

      if (filter.name) params.name = filter.name;
      return this[LIST_CAMPAIGNS]({params, persist: true});
    },
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
        loadData: this.loadCampaigns
      },
      onItemDeleting: onDeleteItem(this.$alertify, this.$ability,
                                   this[DELETE_CAMPAIGN], RESOURCE_NAME),
      fields: this.getGridFields(),
      editItem: (item) => this.onUpdateItem(RESOURCE_NAME,
                                            window.$(`#${this.editModalId}`),
                                            item)
    });
  },
  watch: {
    campaignsList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.campaignsList);
      },
      deep: true
    }
  },
  data() {
    return {
      editedResource: {},
      gridPanelId: "campaignsGrid",
      createModalId: "createDialog",
      editModalId: "editDialog",
      statsModalId: "statsDialog"
    }
  }
}
</script>
