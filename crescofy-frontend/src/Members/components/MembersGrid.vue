<template>
  <div>
      <FormModal :modalId="editModalId" :memberToEdit="editedResource" :modalType="1"/>
      <FormModal :modalId="createModalId" :modalType="2"/>
      <div ref="grid"></div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import { DELETE_MEMBER } from '@/Core/store/action-types';
import { controlField, onDeleteItem } from '@/Core/helpers/gridUtils';
import BaseGridMixin from '../mixins/BaseGridMixin';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { RESOURCE_NAME } from '../member.vars';
import FormModal from './FormModal';

export default {
  name: 'MembersGrid',
  mixins: [BaseGridMixin, GlobalGridMixin],
  components: {FormModal},
  methods: {
    ...mapActions('member', [DELETE_MEMBER]),

    getDetailsBtn(item) {
      return window.$("<input>").attr({
        class: 'jsgrid-button jsgrid-search-button',
        type: 'button'
      })
        .click((e) => {
          this.$router.push({
            name: 'MemberDetail',
            params: { memberId: item.id }
          })
          e.stopPropagation();
        });
    },

    getControlField() {
      var vueContext = this;
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      var control = controlField(showDetailsDialog,
                                 `Register new ${RESOURCE_NAME}`);
      control.itemTemplate = function() {
        var $result = window.jsGrid.fields.control.prototype
                            .itemTemplate.apply(this, arguments);

        let $detailsBtn = vueContext.getDetailsBtn(arguments[1]);
        return $result.add($detailsBtn);
      }

      return control;
    },

    getGridFields() {
      var baseFields = this.gridFields();
      baseFields.push();
      baseFields = baseFields.concat([
        {type: "checkbox", title: "Active Status", width: "10%", name: 'is_active'},
        {type: "text", title: "Email", width: "auto", name: 'email', filtering: false},
        this.getControlField()
      ])
      return baseFields;
    },
  },
  mounted() {
    var options = this.gridOptions()
    options.editItem = (item) => this.onUpdateItem(RESOURCE_NAME,
                                                   window.$(`#${this.editModalId}`),
                                                   item);
    options.onItemDeleting = onDeleteItem(this.$alertify, this.$ability,
                                          this[DELETE_MEMBER], RESOURCE_NAME);
    options.filtering = true;
    options.pageSize = 15;
    this.grid = window.$(this.$refs.grid).jsGrid(options);
  },
  data() {
    return {
      editedResource: {},
      createModalId: "createDialog",
      editModalId: "editDialog"
    }
  }
}
</script>
