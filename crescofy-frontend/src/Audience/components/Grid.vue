<template>
  <div>

      <Modal :modalId="editModalId" :audienceToEdit="editedResource" :modalType="1"/>
      <Modal :modalId="createModalId" :modalType="2"/>

      <div :id='gridPanelId'></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import { LIST_AUDIENCE, DELETE_AUDIENCE } from '@/Core/store/action-types';
import { onDeleteItem, controlField } from '@/Core/helpers/gridUtils';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { RESOURCE_NAME } from '../audience.vars';
import Modal from './Modal';

export default {
  name: 'AudienceGrid',
  mixins: [GlobalGridMixin],
  components: { Modal },
  computed: {
    ...mapGetters('audience', ["audienceList"]),
    ...mapGetters('user', ["userProfile"])
  },
  methods: {
    ...mapActions('audience', [LIST_AUDIENCE, DELETE_AUDIENCE]),

    getGridFields() {
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      return [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Audience name", autosearch: true },
        { name: "members.length", type: "number", width: "auto", title: "Size"},
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
      data: this[LIST_AUDIENCE](),
      onItemDeleting: onDeleteItem(this.$alertify, this.$ability,
                                   this[DELETE_AUDIENCE], RESOURCE_NAME),
      fields: this.getGridFields(),
      editItem: (item) => this.onUpdateItem(RESOURCE_NAME,
                                            window.$(`#${this.editModalId}`),
                                            item)
    });
  },
  watch: {
    audienceList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.audienceList);
      },
      deep: true
    }
  },
  data() {
    return {
      editedResource: {},
      gridPanelId: "audienceGrid",
      createModalId: "createDialog",
      editModalId: "editDialog"
    }
  }
}
</script>
