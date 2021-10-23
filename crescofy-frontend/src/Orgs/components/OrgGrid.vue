<template>
  <div>
      <OrgModal :modalId="editModalId" :orgToEdit="editedResource" :modalType="1"/>
      <OrgModal :modalId="createModalId" :modalType="2"/>
      <div :id='gridPanelId'></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import { LIST_ORGS, DELETE_ORG } from '@/Core/store/action-types';
import { controlField, onDeleteItem } from '@/Core/helpers/gridUtils';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { RESOURCE_NAME } from '../org.vars';
import OrgModal from './OrgModal';

export default {
  name: 'OrgGrid',
  mixins: [GlobalGridMixin],
  components: {
      OrgModal
  },
  computed: {
    ...mapGetters('org', ["orgsList"]),
    ...mapGetters('user', ["userProfile"])
  },
  methods: {
    ...mapActions('org', [LIST_ORGS, DELETE_ORG]),

    getGridFields() {
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      return [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Org name", autosearch: true },
        { name: "id", type: "number", visible: false, width: "auto" },
        controlField(showDetailsDialog, `Register new ${RESOURCE_NAME}`)
      ]
    },
  },

  mounted() {
    this.grid = window.$(`#${this.gridPanelId}`).jsGrid({
      height: "90%",
      width: "100%",
      autoload: true,
      paging: true,
      heading: true,
      editing: false,
      pageSize: 15,
      confirmDeleting: false,
      data: this[LIST_ORGS](),
      onItemDeleting: onDeleteItem(this.$alertify, this.$ability,
                                   this[DELETE_ORG], RESOURCE_NAME),
      fields: this.getGridFields(),
      editItem: (item) => this.onUpdateItem(RESOURCE_NAME,
                                            window.$(`#${this.editModalId}`),
                                            item)
    });
  },

  watch: {
    orgsList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.orgsList);
      },
      deep: true
    }
  },
  data() {
    return {
      editedResource: {},
      gridPanelId: "orgsGrid",
      createModalId: "createDialog",
      editModalId: "editDialog"
    }
  }
}
</script>
