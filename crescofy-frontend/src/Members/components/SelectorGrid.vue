<template>
  <div>
      <div ref="grid"></div>
  </div>
</template>

<script>
import BaseGridMixin from '../mixins/BaseGridMixin';

/**
 * Members Table with built-in selector.
 * Allow to select/deselect rows by on-click event
 */
export default {
  name: 'SelectorMembersGrid',
  mixins: [BaseGridMixin],
  props: {
    preSelectedMemberIds: {
      required: true,
      type: Array,
    }
  },
  emit: ['update'],
  methods: {
    getGridFields() {
      var baseFields = this.gridFields();
      baseFields.push({
        name: "selected", type: "checkbox",  title: "Selected", width: "auto",
        itemTemplate: (value, item) => {
          var check = this.selectedMembers[item.id] ? "checked": "";
          return `<input type="checkbox" ${check} disabled>`;
        }
      })
      return baseFields;
    },

  },
  mounted() {
    var options = this.gridOptions();
    options.rowClick = (args) => {
      if (!this.selectedMembers[args.item.id]) {
        this.selectedMembers[args.item.id] = true;
      } else {
        delete this.selectedMembers[args.item.id];
      }

      this.grid.jsGrid("updateItem", args.item);
      let ids = Object.keys(this.selectedMembers).map(id => parseInt(id));
      this.$emit('update', ids)
    }
    this.grid = window.$(this.$refs.grid).jsGrid(options);
  },
  watch: {
    preSelectedMemberIds: function(ids) {
      this.selectedMembers = {};
      ids.forEach(id => {
        this.selectedMembers[id] = true;
      });

      this.grid.jsGrid("option", "data", this.membersList);
    }
  },
  data() {
    return {
      selectedMembers: {},
    }
  }
}
</script>
