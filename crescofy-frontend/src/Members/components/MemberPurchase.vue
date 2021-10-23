<template>
  <div>
      <div ref="grid"></div>
      <ReceiptDetail :orders="receiptOrders" :modalId="modalId"/>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import { LIST_MEMBER_RECEIPTS, LIST_RECEIPT_ORDERS } from '@/Core/store/action-types';
import ReceiptDetail from './ReceiptDetail';
import '@/Core/helpers/DateRangeField';

export default {
  name: 'MemberPurchaseGrid',
  components: {ReceiptDetail},
  methods: {
    ...mapActions('receipt', [LIST_RECEIPT_ORDERS]),
    ...mapActions('member', [LIST_MEMBER_RECEIPTS]),

    getControlField() {
      return { type: "control", width: "auto", editButton: false,
        deleteButton: false, title: "Detail view",
        itemTemplate: (value, item) => {
          let $detailBtn = window.$("<button>")
            .attr({class: 'jsgrid-button jsgrid-search-button'})
            .click((e) => {
              this[LIST_RECEIPT_ORDERS]({objId: item.id}).then(data => {
                // open detail modal window
                this.receiptOrders = data;
                window.$(`#${this.modalId}`).modal('toggle');
              })

              e.stopPropagation();
            });

          return window.$("<div>").append($detailBtn);
        }
      }
    },

    getGridFields() {
      return [
        { name: "order_date", type: "daterange", width: "auto", sorting: true,
          title: "Receipt date", autosearch: true,
          itemTemplate: (value) => value },
        { name: "id", type: "number", width: "auto", filtering: false },
        this.getControlField()
      ]
    },

    loadPurchase(filter) {
      let params = {order: '-order_date'};
      if (filter.order_date) {
        params.date_after = filter.order_date.start_date;
        params.date_before = filter.order_date.end_date;
      }
      return this[LIST_MEMBER_RECEIPTS]({
        params,
        objId: this.$route.params.memberId
      });
    }
  },

  mounted() {
    this.grid = window.$(this.$refs.grid).jsGrid({
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
        loadData: this.loadPurchase
      },
      fields: this.getGridFields(),
    });
  },

  data() {
    return {
      receiptOrders: [],
      modalId: 'receiptDetails'
    }
  }
}
</script>
