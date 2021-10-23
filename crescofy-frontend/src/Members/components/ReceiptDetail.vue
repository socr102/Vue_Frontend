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
      <div class="modal-body">
          <div class="table-responsive">
            <div ref="grid"></div>
          </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'ReceiptDetail',
  props: {
    modalId: {
      required: true,
      type: String,
    },
    orders: {
      required: true,
      type: Array,
    },
  },
  methods: {
    getGridFields() {
      return [
        { name: "count", type: "text", width: "auto", title: "Items count", },
        { name: "currency", type: "number", width: "auto", title: "Currency",},
        { name: "item_price", type: "number", width: "auto", title: "Item Price"},
        { name: "article.name", type: "number", width: "auto", title: "Article"},
        { name: "store.name", type: "number", width: "auto", title: "Store"},
        { name: "id", type: "number", visible: false, width: "auto" },
      ]
    }
  },

  mounted() {
    this.grid = window.$(this.$refs.grid).jsGrid({
      height: "90%",
      width: "100%",
      autoload: true,
      paging: true,
      heading: true,
      editing: false,
      pageSize: 15,
      confirmDeleting: false,
      data: this.orders,
      fields: this.getGridFields(),
    });
  },

  watch: {
    orders: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.orders);
      },
      deep: true
    }
  },

  data() {
    return {
      header_text: "Member Orders"
    }
  }
}
</script>
